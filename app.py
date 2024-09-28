import sys
import os

# Add the subdirectory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "arc_finetuning_st", "streamlit"))

# Import and run the Streamlit app from the subdirectory
if __name__ == "__main__":
    import app
