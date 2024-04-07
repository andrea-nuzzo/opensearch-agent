from typing import List, Any
from pydantic.v1 import BaseModel, Field
from langchain.tools import StructuredTool
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

folder_plot_path = os.getenv("FOLDER_PLOT_PATH")

class PlotInput(BaseModel):
    """Input for the plot generation tool."""
    plot_type: str = Field(..., description="Type of plot to generate (e.g., 'bar', 'line').")
    data: List[object] = Field(..., description="An array representing the data to be entered on the plot. The first key of the object will be named 'x' while the second key 'y'")

def open_search_plot(plot_type: str,  data: List[Any]) -> str:
        """Generate a plot based on the provided data."""

        x_values = [item['x'] for item in data]
        y_values = [item['y'] for item in data]

        plt.figure(figsize=(10, 6))
        if plot_type == "bar":
            plt.bar(x_values, y_values)
        elif plot_type == "line":
            plt.plot(x_values, y_values)

        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plot_path = os.path.join(folder_plot_path, "plot.png")

        plt.savefig(plot_path)
        plt.close()

        return plot_path
    
    
def create_plot_tool():
    return StructuredTool.from_function(open_search_plot, name="opensearch_plot_data_tool", args_schema=PlotInput)
