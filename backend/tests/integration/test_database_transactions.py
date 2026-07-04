"""
Integration tests for database transaction atomicity and integrity.

These tests ensure that financial operations are atomic and handle
concurrency correctly.
"""

import pytest
import threading
from sqlmodel import Session
from src.services.sale_service import SaleService
from src.models.sales import SaleCreate, SaleItemCreate, PaymentMethod
from src.models.inventory import Product


@pytest.mark.integration
@pytest.mark.financial
class TestSaleAtomicity:
    """Test that sale transactions are atomic (all-or-nothing)."""

    def test_sale_rollback_on_error(self, session, settings, admin_user, product):
        """Simulate error during sale, verify stock not deducted."""
        initial_stock = product.stock_quantity

        # Create sale with insufficient stock
        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=initial_stock + 10)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        # Attempt to create sale (should fail)
        with pytest.raises(Exception):
            SaleService.create_sale(session, sale_in, admin_user.id)
            session.commit()

        # Rollback the failed transaction
        session.rollback()

        # Verify stock unchanged
        session.refresh(product)
        assert product.stock_quantity == initial_stock

    def test_partial_failure_rollback(self, session, settings, admin_user, sample_products):
        """Sale with multiple items where one fails should rollback all stock changes."""
        # Set first product with sufficient stock
        sample_products[0].stock_quantity = 10
        session.add(sample_products[0])

        # Set second product with insufficient stock
        sample_products[1].stock_quantity = 1
        session.add(sample_products[1])
        session.commit()

        initial_stocks = {
            sample_products[0].id: sample_products[0].stock_quantity,
            sample_products[1].id: sample_products[1].stock_quantity,
        }

        # Create sale with multiple items (second item will fail)
        sale_in = SaleCreate(
            customer_id=None,
            items=[
                SaleItemCreate(product_id=sample_products[0].id, quantity=5),  # OK
                SaleItemCreate(product_id=sample_products[1].id, quantity=5),  # FAIL (only 1 available)
            ],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        # Attempt to create sale (should fail on second item)
        with pytest.raises(Exception):
            SaleService.create_sale(session, sale_in, admin_user.id)
            session.commit()

        # Rollback
        session.rollback()

        # Verify both products' stock unchanged (transaction rolled back)
        session.refresh(sample_products[0])
        session.refresh(sample_products[1])
        assert sample_products[0].stock_quantity == initial_stocks[sample_products[0].id]
        assert sample_products[1].stock_quantity == initial_stocks[sample_products[1].id]


@pytest.mark.integration
@pytest.mark.financial
@pytest.mark.slow
class TestConcurrentSales:
    """Test concurrent sales of the same product."""

    def test_concurrent_sales_same_product(self, engine, settings, admin_user, category):
        """Two simultaneous sales of 5 units, stock=8 → one succeeds, one fails."""
        # Create a fresh product in database with stock=8
        with Session(engine) as setup_session:
            product = Product(
                name="Concurrent Test Product",
                sku="CONC-001",
                category_id=category.id,
                selling_price=100.0,
                cost_price=50.0,
                stock_quantity=8,
                reorder_level=5,
                unit="pcs"
            )
            setup_session.add(product)
            setup_session.commit()
            setup_session.refresh(product)
            product_id = product.id

        results = {"success": 0, "failed": 0, "errors": []}

        def attempt_sale(session_factory, product_id, admin_user_id):
            """Attempt to create a sale in a separate session."""
            try:
                with Session(session_factory) as thread_session:
                    sale_in = SaleCreate(
                        customer_id=None,
                        items=[SaleItemCreate(product_id=product_id, quantity=5)],
                        discount_amount=0,
                        payment_method=PaymentMethod.CASH
                    )
                    SaleService.create_sale(thread_session, sale_in, admin_user_id)
                    thread_session.commit()
                    results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(str(e))

        # Create two threads that attempt to sell simultaneously
        thread1 = threading.Thread(target=attempt_sale, args=(engine, product_id, admin_user.id))
        thread2 = threading.Thread(target=attempt_sale, args=(engine, product_id, admin_user.id))

        # Start both threads
        thread1.start()
        thread2.start()

        # Wait for both to complete
        thread1.join()
        thread2.join()

        # Verify: One should succeed, one should fail (stock=8, each wants 5)
        # Both could technically succeed if stock is enough, but at least verify integrity
        # With stock=8 and each sale taking 5, only one should succeed
        assert results["success"] == 1
        assert results["failed"] == 1

        # Verify final stock is correct
        with Session(engine) as verify_session:
            product = verify_session.get(Product, product_id)
            # One sale succeeded (5 units), so stock should be 8 - 5 = 3
            assert product.stock_quantity == 3

    def test_sequential_vs_concurrent_stock_consistency(self, engine, settings, admin_user, category):
        """Verify that stock deduction is consistent regardless of concurrency."""
        # Create product with sufficient stock
        with Session(engine) as setup_session:
            product = Product(
                name="Sequential Test Product",
                sku="SEQ-001",
                category_id=category.id,
                selling_price=100.0,
                cost_price=50.0,
                stock_quantity=100,
                reorder_level=10,
                unit="pcs"
            )
            setup_session.add(product)
            setup_session.commit()
            setup_session.refresh(product)
            product_id = product.id

        # Perform 10 sales of 5 units each concurrently
        threads = []
        success_count = [0]  # Use list for mutable counter

        def make_sale(session_factory, product_id, admin_user_id):
            try:
                with Session(session_factory) as thread_session:
                    sale_in = SaleCreate(
                        customer_id=None,
                        items=[SaleItemCreate(product_id=product_id, quantity=5)],
                        discount_amount=0,
                        payment_method=PaymentMethod.CASH
                    )
                    SaleService.create_sale(thread_session, sale_in, admin_user_id)
                    thread_session.commit()
                    success_count[0] += 1
            except Exception:
                pass  # Some may fail due to race conditions

        for _ in range(10):
            t = threading.Thread(target=make_sale, args=(engine, product_id, admin_user.id))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify final stock
        with Session(engine) as verify_session:
            product = verify_session.get(Product, product_id)
            expected_stock = 100 - (success_count[0] * 5)
            assert product.stock_quantity == expected_stock


@pytest.mark.integration
class TestTransactionIsolation:
    """Test transaction isolation levels."""

    def test_uncommitted_changes_not_visible(self, engine, settings, admin_user, product):
        """Changes in one session should not be visible to another until committed."""
        product_id = product.id
        original_stock = product.stock_quantity

        # Session 1: Make a change but don't commit
        with Session(engine) as session1:
            product1 = session1.get(Product, product_id)
            product1.stock_quantity -= 10
            session1.add(product1)
            session1.flush()  # Flush but don't commit

            # Session 2: Check if change is visible (should see original value)
            with Session(engine) as session2:
                product2 = session2.get(Product, product_id)
                assert product2.stock_quantity == original_stock

            # Rollback session 1
            session1.rollback()

        # Verify stock unchanged
        with Session(engine) as verify_session:
            product_verify = verify_session.get(Product, product_id)
            assert product_verify.stock_quantity == original_stock

    def test_committed_changes_visible(self, engine, admin_user, product):
        """Committed changes should be visible to other sessions."""
        product_id = product.id

        # Session 1: Make a change and commit
        with Session(engine) as session1:
            product1 = session1.get(Product, product_id)
            product1.stock_quantity -= 10
            session1.add(product1)
            session1.commit()
            new_stock = product1.stock_quantity

        # Session 2: Verify change is visible
        with Session(engine) as session2:
            product2 = session2.get(Product, product_id)
            assert product2.stock_quantity == new_stock
