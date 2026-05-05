import csv
import io
from typing import List, Dict, Any
from fastapi.responses import StreamingResponse

class ExportUtility:
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filename: str) -> StreamingResponse:
        """
        Converts a list of dictionaries into a CSV response.
        Uses Python's built-in csv module (no pandas dependency).
        """
        stream = io.StringIO()
        if data:
            writer = csv.DictWriter(stream, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        response = StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv"
        )
        response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"
        return response

    @staticmethod
    def to_excel(data: List[Dict[str, Any]], filename: str) -> StreamingResponse:
        """
        Converts a list of dictionaries into an Excel response.
        Falls back to CSV if openpyxl/pandas not available.
        """
        try:
            import pandas as pd
            df = pd.DataFrame(data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            response = StreamingResponse(
                iter([output.getvalue()]),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response.headers["Content-Disposition"] = f"attachment; filename={filename}.xlsx"
            return response
        except ImportError:
            # Fall back to CSV if pandas/openpyxl not installed
            return ExportUtility.to_csv(data, filename)
