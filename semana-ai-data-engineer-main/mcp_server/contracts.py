from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, model_validator


class TaskResponse(BaseModel):
    status: Literal["success", "error"]
    task: Optional[str] = None
    result: Optional[Any] = None
    message: Optional[str] = None
    trace_id: str

    @model_validator(mode="after")
    def validate_output(self):
        """
        Enforce output quality for successful tasks.
        """

        # Only validate successful responses
        if self.status != "success" or not self.result:
            return self

        output = str(self.result)

        # --- BUSINESS ANALYSIS ---
        if self.task == "business_analysis":

            # Executive mode detection (by content)
            if "EXECUTIVE SUMMARY" in output:
                required = [
                    "Average Order Value",
                    "Top",
                    "Payment",
                ]

                missing = [r for r in required if r not in output]
                
                if missing:
                    raise ValueError(f"Invalid executive summary: missing {missing}")

            # Exploration mode
            else:
                if "COUNTS" not in output:
                    raise ValueError("Invalid exploration output: missing COUNTS")

        # --- REVIEWS ---
        if self.task == "analyze_reviews":
            if "REVIEW STRUCTURE" not in output:
                raise ValueError("Invalid reviews output: missing structure")

            if "SENTIMENT DISTRIBUTION" not in output:
                raise ValueError("Invalid reviews output: missing sentiment")

        return self