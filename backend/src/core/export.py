import pandas as pd
import io
from typing import List, Dict, Any
from fastapi.responses import StreamingResponse

class ExportUtility:
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filename: str) -> StreamingResponse:
        """
        Converts a list of dictionaries into a CSV response.
        """
        if not data:
            # Return empty CSV with headers if possible or just empty
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(data)
            
        stream = io.StringIO()
        df.to_csv(stream, index=False)
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
        Note: Requires openpyxl.
        """
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
