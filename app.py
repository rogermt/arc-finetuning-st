from arc_finetuning_st.streamlit.app import main
from litellm_proxy.server import start

if __name__ == "__main__":
    start()
    main()
