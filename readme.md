# Welcome to the Rootcode Anonymization Pipeline

## How to Install

1. **Git Clone the Repository:**
   - Navigate to any directory where you would like to keep the project and execute the following command to clone the repository:
     ```
     git clone https://github.com/rootcodelabs/rootcode-anonymizer.git
     ```

2. **Setup the Base Model:**
   - Before proceeding with the installation, please download the NER_basemodel.zip from [this link](https://drive.google.com/file/d/1v6Xvkr_t4G2mGC3bfKORXHhGciEUwptM/view?usp=sharing) and place it in the root directory of the cloned repository. Then, unzip the file. This zip file contains the model for Named Entity Recognition (NER). Note that without this base model, the anonymizer will not work.

3. **Installation Methods:**
   - There are two ways to install:
     - Using Python
     - Using Docker

### Installing using Python

1. **Create Python Environment:**
   - First, create an environment with Python version 3.9.19.

2. **Install Requirements:**
   - Install the required packages specified in the `requirements.txt` file using the following command:
     ```
     pip install --no-cache-dir -r requirements.txt
     ```

3. **Launch the Application:**
   - Launch the application using the following command:
     ```
     streamlit run Anonymizer_application.py
     ```
   - In most cases, this will open a browser window directing you to the application. Alternatively, you can visit [http://localhost:8501](http://localhost:8501) to access the application.

### Installing using Docker

1. **Install Docker:**
   - Ensure Docker is installed on your computer. If not, please install Docker first.

2. **Build Docker Container:**
   - Navigate to the cloned repository and execute the following command to build the Docker container:
     ```
     docker build -t anonymizer-app .
     ```
   - This process may take a few minutes.

3. **Start the Container:**
   - Once the build process is completed, start the container using the following command:
     ```
     docker run -p 8501:8501 anonymizer-app
     ```
   - You can visit http://localhost:8501 to access the application.

4. **Stopping the Container:**
   - When you need to stop the container, use the following command:
     ```
     docker stop anonymizer-app
     ```

This pipeline provides an effective solution for anonymizing data. Enjoy anonymizing your data seamlessly!

## Usage

Sometimes when you access [http://localhost:8501](http://localhost:8501), you might encounter a loading screen, as shown below:

![Loading Screen](https://github.com/rootcodelabs/rootcode-anonymizer/assets/51948729/d0c923be-3ae0-4056-9287-50f0a890fe8c)

After loading, you will be presented with the main screen, where you'll find three options in the sidebar:

- **Anonymizer**
- **Regex**
- **Immutable Words**

### Anonymizer

This component allows you to anonymize text. Simply click on "Browse files" to select a .csv file, or drag and drop a csv file onto the interface. 
![Upload Screen](https://github.com/rootcodelabs/rootcode-anonymizer/assets/51948729/2ee6bdb9-1235-4ff1-879f-3e884d76ebcf)

Once the file is provided, Anonymizer will start processing it like this:
![Processing Screen](https://github.com/rootcodelabs/rootcode-anonymizer/assets/51948729/076883ad-90e9-4434-aef2-8cab564fdd84)

This might take a lot of time depending on the csv file provided and system requirements. After processing, the system will allow you to download the anonymized file:

![Done Screen](https://github.com/rootcodelabs/rootcode-anonymizer/assets/51948729/34c7a4dc-2606-4880-86d4-4e1ca5693a18)

### Regex Management

Anonymizer can detect given regex patterns and replace them with a specified replacement string. Here you can view, update, and delete existing regex patterns and replacements, as well as add completely new ones.
![regex_management](https://github.com/rootcodelabs/rootcode-anonymizer/assets/51948729/64af1b36-45ca-4628-874c-c9a01e22a974)

### Immutable Words Management

If there are certain words that Anonymizer should not anonymize, you can manage those words here. You can view, update, and delete existing words, as well as add new ones.

![Immutable_word_management](https://github.com/rootcodelabs/rootcode-anonymizer/assets/51948729/e958313b-0191-4cdc-83a7-563277f84ddb)

**Important Points:**
- When anonymization is happening on the Anonymizer tab, do not change tabs to Regex or Immutable Words, as this will cause you to lose results of the anonymization.
