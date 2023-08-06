# Bridge GPT

BridgeGPT is a Streamlit application that uses the GPT-2 pretrained model from Huggingface to generate text based on user input.

## Dependencies

The following dependencies are needed to run the application:

* Python 3.x
* Streamlit 1.19.0
* Tensorflow 2.11.0
* Transformers 4.26.1

## Installation

You can install Bridge GPT using pip. Open your terminal and run the following command:
   ```
   pip install bridgeaihub
   ```

## Usage

To use Bridge GPT in a Python file (eg: pythonfile.py), load the load_template function from the bridgeaihub package using the following code:
   ```
   import bridgeaihub as bah

   bah.load_template()
   ```
Run the following command in your terminal:
   ```
   streamlit run pythonfile.py
   ```
This will start the Bridge GPT app in your web browser. Input a prompt into the text box provided, and specify the maximum number of characters needed in the generated text, then click the "Generate Text" button. Bridge GPT will use the GPT-2 model to generate text based on your input and parameters.