# 🌿 LiteFarm-MDS-Capstone

## 👀 Challenge and Our vision  

Climate change poses a critical challenge to the sustainability of our planet, largely due to rising greenhouse gas (GHG) emissions. Agriculture is a major contributor, with activities such as livestock rearing, fertilizer use, and land management practices contributing heavily to GHG emissions. Quantifying agricultural GHG emissions can help optimize farming practices from crop selection to tillage methods, thereby reducing emissions. Our broader objective is to empower stakeholders, including farmers, researchers, and policymakers to make data-driven decisions, transforming sustainability into a measurable and actionable goal.

## 💡 Project Overview  

The project aims to refine and enhance existing GHG modeling for the LiteFarm platform, specifically focusing on nitrous oxide ($N_2O$) emissions. The project has two main objectives. First, the initiative aims to improve existing modeling framework to incorporate dynamic global data for greater accuracy and broader applicability. Second, the project will conduct sensitivity analysis to identify influential factors on emissions estimation to guide targeted data collection. Deliverables will feature an updated dashboard for visualizing emissions and a Python script for automated data integration and GHG calculation. Ultimately, we aim to provide actionable insights for stakeholders, aiding decision-making in sustainable agricultural practices.

## 📖 Installation

### Step 1: Clone the Repository

Start by cloning the repository to your local machine. Open your terminal and run the following command:

``` bash
$ git clone git@github.com:yhan178/LiteFarm-MDS-Capstone.git
```

Navigate to the directory of the cloned repository.

### Step 2: Create and Activate the Conda Environment

Create a new Conda environment using the `environment.yml` file provided in this repository. To create the environment, open your terminal and navigate to the directory where the `environment.yml` file is located. Then, run the following command:

``` bash
$ conda env create -f environment.yml

$ conda activate LiteFarmGHG
```

### Step 3: Download Supporting Data  

After cloning the repository, you need to download external data for finer resolution global soil texture analysis. Please follow these steps to download and set up the data:

#### Download the Data:  

Visit the following link to download the raster file for Harmonized World Soil Database v2.0:
[HWSD2 RASTER Data](https://s3.eu-west-1.amazonaws.com/data.gaezdev.aws.fao.org/HWSD/HWSD2_RASTER.zip).

#### Extract the Files:  

Once the download is complete, unzip the file. You should have the following four files: `HWSD2.bil`, `HWSD2.hdr`, `HWSD2.prj`, `HWSD2.stx`.

#### Place the Files in the Repository:  

Navigate to the `data/HWSD2_RASTER` directory within the cloned repository. If this directory does not exist, create it. Move all extracted files into this directory.

For more details about the dataset, including its structure and usage, visit the [Harmonized World Soil Database v2.0](https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v20/en/). By following these steps, you ensure that the project has the necessary data to perform analysis.

## 💻 Usage

### 1. Running the N<sub>2</sub>O Emission Calculator - Farmer's Mode

Run the calculator with default operation mode (farmer), source (default climate data at the ecodistrict level) with default output filename (output.json). The output file is stored in folder `data/outputs`:

```bash
$ python src/main.py -i data/test/litefarm_test.csv --farm_id 0369f026-1f90-11ee-b788-0242ac150004 --crop Soybean
```

Run the calculator with default operation mode (farmer) and external source (external sources for climate and soil data specific to farm location) with user-define file name. The output file is stored in folder `data/outputs`:

``` bash
$ python src/main.py -i data/test/litefarm_test.csv --farm_id 0369f026-1f90-11ee-b788-0242ac150004 --crop Soybean --operation_mode farmer --source external -o my_farm_precise_climate_data.json
```

### 2. Running the N<sub>2</sub>O Emission Calculator - Scientific Mode

Run the calculator with sensitivity analysis settings. The output file is stored in folder `data/outputs`:

``` bash
$ python src/main.py -i data/test/litefarm_test.csv --farm_id 0369f026-1f90-11ee-b788-0242ac150004 --crop Soybean --operation_mode scientific --source external --num_runs 100 -o farm_100_run_sci_mode.json 
```

### Explanation of Command-Line Arguments

Below are detailed descriptions of each command-line argument you can use with the N<sub>2</sub>O Emission Calculator.

- **-i, --input** (required): Specifies the path to the input file, which can be either a CSV or JSON file containing the necessary farm data for calculations.
  - Additionally, if you need to create farm records interactively, you can use the `input_farm_record.py` script located in the `scripts` folder. This script allows you to manually enter new farm data, which will be saved to a JSON file as new records. You can also use script `generate_farm_data.py` in the `scripts` folder to manually add new farm record to a JSON file. 

- **--farm_id** (required): Specifies the unique identifier for the farm. This identifier must match one listed in the input CSV or JSON file. The program uses this ID in conjunction with `--crop` to precisely locate and retrieve the farm's data.

- **--crop** (required): Specifies the type of crop planted at the farm. This crop name must be one associated with the specified `farm_id` in the input CSV or JSON file. Together, the `farm_id` and `crop` serve as keys to fetch the detailed data needed for calculations.

- **-o, --output**  (optional): Name of the output JSON file where the results will be saved. If this argument is not specified, the program will default to saving the results in `output.json` in the `outputs` directory. 

- **--operation_mode** (optional): Choose between `farmer` and `scientific` operational modes:
  - `farmer`: Standard operational mode, designed to provide definitive N<sub>2</sub>O emissions calculations based on specified farm data. This mode delivers clear, final results for each run, ideal for everyday farming decisions.
  - `scientific`: Designed for research purposes, this mode facilitates a sensitivity analysis by performing multiple simulations (defined by `num_runs`) to explore how various parameters influence N<sub>2</sub>O emissions. This approach helps identify critical factors affecting emissions estimates.

- **--source** (optional): This argument defines the precision level of the climate parameters, specifically precipitation, evapotranspiration, and soil texture, used in the calculations. The operational modes available are:
  - `default`: This mode uses climate data aggregated at the ecodistrict level. If not specified, the mode will default to `default` mode.
  - `external`: Select this mode to obtain climate data specific to the exact farm location as well (and the sampled points in `scientific` operation mode). This setting provides potentially more accurate emissions calculations. Mandatory for `scientific` mode.

- **--num_runs** (optional): Number of simulation runs, applicable only in `scientific` mode.

- **--sampl_modifier**, **--sampl_crop**, **--sampl_crop_group** (optional): Define how parameters are sampled in scientific mode, adjusting the variability and distribution of model inputs:
  - `default`: Currently uses a uniform distribution ranging from 0.75 to 1.25 times the base value of each parameter, providing a balanced range of variability.
  - `user_define`: Allows users to specify custom parameter distributions. Editable Python scripts for defining distribution of parameters are located in the `scripts` folder, and the generated distributions are stored as JSON files in folder `data/params_sampling_range`. Users should adjust these distributions as needed prior to executing this program to tailor the sensitivity analysis to research requirements.

#### Viewing Help Information  

You can also view the help message for details about the command-line arguments with the following command:

```bash
$ python src/main.py --help
```

## 🧪 Testing

To ensure that all components of the project are working correctly, you can run the tests provided in the `tests` directory. These tests check the functionality of various modules and ensure that changes do not break existing features.

To run the tests, navigate to the root of the repository and execute the following command in your terminal:

```bash
pytest tests/*
```

To run the tests without displaying warnings, execute:

```bash
pytest tests/* -p no:warnings
```

## 📚 Folder Structure  

```plaintext
LiteFarm-MDS-Capstone/
├── data/
│   ├── external/
│   │   └── Includes external soil data and shapefiles for geographic visualization.
│   ├── outputs/
│   │   └── Includes output files of emissions calculation.
│   ├── params_sampling_range/
│   │   └── Includes user-defined parameter distributions.
│   ├── preprocessed/
│   │   └── Data that has been cleaned and preprocessed.
│   ├── raw/
│   │   └── Raw data and tables from Holos and LiteFarm.
│   └── temp/
│   │   └── Stores intermediate files used during data processing, not included in final outputs.
│   └── test/
│       └── CSV files with hypothetical farm data for testing and sensitivity analysis.
├── docs/
│   └── Markdown files explaining data and code usage.
├── img/
│   └── Store images and figures used for reports.
├── notebooks/
│   └── Jupyter notebooks for EDA and experiments.
├── reports/
│   └── Contains all project reports, including presentation slides, proposals, and final reports.
├── scripts/
│   └── Contains supporting scripts for users to defined desired parameter distributions and run batch processing for large-scale farm data under `scientific` mode.
├── src/
│   ├── main.py
│   │   └── The main script of the project.
│   └── data_loader/
│   │   └── Code modules for retrieving data for calculation
│   └── calculator/
│       └── Code modules for calculating N2O emissions
├── tests/
│   └── Tests to ensure the code works as expected.
├── README.md
├── LICENSE
├── Code of Conduct.md
└── environment.yml
```

## 🪜 How to get support?  

Need help or feedback? Open an issue on our GitHub – we're ready to assist your journey towards informed actions for sustainable agriculture.

## 👥 Contributors  

-   Yi Han ([\@yhan178](https://github.com/yhan178))
-   Hancheng Qin ([\@hchqin](https://github.com/hchqin))
-   He Ma ([\@hema2022ubc](https://github.com/hema2022ubc))

## ©️ License  

This LiteFarm GHG emission project was developed by He Ma, Hancheng Qin, and Yi Han. It is licensed under the terms of the [MIT license](LICENSE).
