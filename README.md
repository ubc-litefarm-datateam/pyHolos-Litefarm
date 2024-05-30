# 🌿 LiteFarm-MDS-Capstone

## 👀 Challenge and Our vision  
Climate change poses a critical challenge to the sustainability of our planet, largely due to rising greenhouse gas (GHG) emissions. Agriculture is a major contributor, with activities such as livestock rearing, fertilizer use, and land management practices contributing heavily to GHG emissions. Quantifying agricultural GHG emissions can help optimize farming practices from crop selection to tillage methods, thereby reducing emissions. Our broader objective is to empower stakeholders, including farmers, researchers, and policymakers to make data-driven decisions, transforming sustainability into a measurable and actionable goal.

## 💡 Project Overview  
The project aims to refine and enhance existing GHG modeling for the LiteFarm platform, specifically focusing on nitrous oxide ($N_2O$) emissions. The project has two main objectives. First, the initiative aims to improve existing modeling framework to incorporate dynamic global data for greater accuracy and broader applicability. Second, the project will conduct sensitivity analysis to identify influential factors on emissions estimation to guide targeted data collection. Deliverables will feature an updated dashboard for visualizing emissions and a Python script for automated data integration and GHG calculation. Ultimately, we aim to provide actionable insights for stakeholders, aiding decision-making in sustainable agricultural practices.

## 📚 Folder Structure  
- `data/`: Store datasets.
    - `raw/`: Farm-related data from LiteFarm.
    - `external/`: external datasets, including climate, soil, crop-related data, along with shapefiles for geographic visualization.
    - `preprocessed/`: Data has been cleaned and preprocessed.
    - `temp/`: Stores intermediate files used during data processing, not included in final outputs.
- `docs/`: Markdown files explaining data and code usage.
- `img/`: Store images and figures used for reports.
- `notebooks/`: Jupyter notebooks for EDA and experiments.
- `reports/`: Contains all project reports, such as presentation slides, proposal, and final reports.
- `src/`: Source code for the project.
    - `main.py`: The main script of the project.
    - `modules/`: Smaller code modules, each serving a function or components of the project.
- `tests/`: Unit tests to ensure the code works as expected.
- `README.md`: Providing an overview of the project, setup instructions, and usage details.
- `LICENSE`: The repository is under the MIT License for now.
- `Code of Conduct.md`: Outlines expectations for participation.
- `environment.yml`: Specifies all dependencies required by the project, facilitating reproducibility and consistency across environments.

## Installation

### Step 1: Clone the Repository

Start by cloning the repository to your local machine. Open your terminal and run the following command:

``` bash
$ git clone git@github.com:yhan178/LiteFarm-MDS-Capstone.git
```

Navigate to the directory of the cloned repository.

### Step 2: Create and Activate the Conda Environment

Create a new Conda environment using the `environment.yaml` file provided in this repository. To create the environment, open your terminal and navigate to the directory where the `environment.yml` file is located. Then, run the following command:

``` bash
$ conda env create -f environment.yml

$ conda activate LiteFarmGHG
```

### Step 3: Running the N<sub>2</sub>O Emission Calculator (Farmer's Mode)

Once you have set up your environment and are ready to run the calculator, you can execute `main.py`. 

#### Explanation of Command-Line Arguments

Below are detailed descriptions of each command-line argument you can use with the N<sub>2</sub>O Emission Calculator.

- **-i, --input** (required): Specifies the path to the input file, which can be either a CSV or JSON file containing the necessary farm data for calculations.
  - Additionally, if you need to create farm records interactively, you can use the `input_farm_record.py` script located in the `scripts` folder. This script allows you to manually enter new farm data, which will be saved to a JSON file as new records.

- **--farm_id** (required): Unique identifier for the farm. This ID must correspond to one listed in the provided input CSV file. The program will use this ID to fetch relevant data from the file.

- **-o, --output**  (optional): Name of the output JSON file where the results will be saved. If this argument is not specified, the program will default to saving the results in `output.json` in the `outputs` directory. 

- **--operation_mode** (optional): Choose between `farmer` and `scientific` operational modes:
  - `farmer`: Standard operational mode, designed to provide definitive N<sub>2</sub>O emissions calculations based on specified farm data. This mode delivers clear, final results for each run, ideal for everyday farming decisions.
  - `scientific`: Designed for research purposes, this mode facilitates a sensitivity analysis by performing multiple simulations (defined by `num_runs`) to explore how various parameters influence N<sub>2</sub>O emissions. This approach helps identify critical factors affecting emissions estimates.

- **--source** (optional): This argument defines the precision level of the climate parameters, specifically precipitation, evapotranspiration, and soil texture, used in the calculations. The operational modes available are:
  - `default`: This mode uses climate data aggregated at the ecodistrict level. If not specified, the mode will default to `default` mode.
  - `external`: Select this mode to obtain climate data specific to the exact farm location as well (and the sampled points in `scientific` operation mode). This setting provides potentially more accurate emissions calculations. Mandatory for `scientific` mode.

- **--num_runs** (optional): Number of simulation runs, applicable only in `scientific` mode.

- **--sampl_modifier**, **--sampl_crop**, **--sampl_crop_group** (optional): Define how parameters are sampled in scientific mode, adjusting the variability and distribution of model inputs:
  - 'default': Currently uses a uniform distribution ranging from 0.75 to 1.25 times the base value of each parameter, providing a balanced range of variability.
  - 'user_define': Allows users to specify custom parameter distributions. Editable Python scripts for defining distribution of parameters are located in the `scripts` folder, and the generated distributions are stored as JSON files in folder `data/params_sampling_range`. Users should adjust these distributions as needed prior to executing this program to tailor the sensitivity analysis to research requirements.
 
##### Viewing Help Information
You can also view the help message for details about the command-line arguments with the following command:

```bash
$ python src/main.py --help
```

#### Usage Example

#### Farmer's Mode

Run the calculator with default operation mode (farmer), source (default climate data at the ecodistrict level) and output filename:

```bash
$ python src/main.py -i data/test/litefarm_test.csv --farm_id 0369f026-1f90-11ee-b788-0242ac150004
```

Run the calculator with default operation mode (farmer) and external source (external sources for climate and soil data specific to farm location):

``` bash
$ python src/main.py -i data/test/litefarm_test.csv --farm_id 0369f026-1f90-11ee-b788-0242ac150004 --mode precise -o my_farm_precise_climate_data.json
```

#### Scientific Mode

Run the calculator with sensitivity analysis settings:

``` bash
$ python src/main.py -i data/test/litefarm_test.csv --farm_id 0369f026-1f90-11ee-b788-0242ac150004 -o my_farm_sci_mode.json --operation_mode scientific --source external --num_runs 100
```

## Developer's Guide  
To be filled.

## 👥 Contributors  
-   Yi Han ([\@yhan178](https://github.com/yhan178))
-   Hancheng Qin ([\@hchqin](https://github.com/hchqin))
-   He Ma ([\@hema2022ubc](https://github.com/hema2022ubc))

## ©️ License  
This LiteFarm GHG emission project was developed by He Ma, Hancheng Qin, and Yi Han. It is licensed under the terms of the [MIT license](LICENSE).
