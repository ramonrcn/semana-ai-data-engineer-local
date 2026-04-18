from mcp_server.tasks.database import business_analysis
from mcp_server.tasks.reviews import reviews_analysis
from mcp_server.tasks.reviews import reviews_summary
from mcp_server.tasks.reviews import analyze_reviews_task
from mcp_server.tasks.models import get_models

TASKS = {
    "business_analysis": business_analysis,
    "reviews_analysis": reviews_analysis,
    "reviews_summary": reviews_summary,
    "analyze_reviews": analyze_reviews_task,  
    "get_models": get_models,
}