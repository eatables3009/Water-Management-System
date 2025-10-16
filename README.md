# Urban Water Management & Flood Mitigation System 💧

This project is an integrated Python-based toolkit for managing urban water resources. It combines a proactive flood mitigation system with a conceptual water distribution simulator to address two critical aspects of urban water management: handling excess water (flooding) and managing essential water supply.

##  Key Features

* **Predictive Flood Analysis**: Uses a machine learning model (Ridge Regression) to predict rainfall intensity based on historical weather data.
* **Geospatial Correlation**: Identifies high-risk flood zones by correlating the locations of lakes with known vulnerable areas.
* **Proactive Mitigation Planning**: When heavy rain is predicted, the system automatically identifies the nearest Sewage Treatment Plant (STP) to each vulnerable zone and generates a mitigation plan.
* **Real-time Vulnerability Check**: A client-server application with a simple GUI allows users to input their coordinates and instantly check if they are in a predicted flood-prone area.
* **Water Distribution Simulation**: Includes a separate module using a Markov Decision Process (MDP) to model and simulate the logistics of a municipal water distribution network.

---

##  System Architecture & Workflow

The flood mitigation system operates in a clear, sequential workflow:

1.  **Analysis & Prediction (`Integrated.py`)**: This script is the core engine. It reads geospatial data for lakes, vulnerable spots, and STPs. It then trains a weather prediction model. If the model predicts heavy rainfall, it generates the `output.csv` file containing a list of vulnerable zones and their nearest STP.

2.  **Server Initialization (`server.py`)**: The server script loads the `output.csv` mitigation plan into memory and starts a TCP server, listening for client connections.

3.  **Client Interaction (`client working.py`)**: A user launches the Tkinter GUI application. They enter a latitude and longitude and click "Search." The client sends these coordinates to the server.

4.  **Verification & Response**: The server receives the coordinates, checks them against the loaded list of vulnerable zones, and sends a response back to the client, which then displays a message indicating if the area is safe or flood-prone.

The **Water Distribution Simulation (`dist system.py`)** is a standalone script that models a different aspect of water management and is not directly connected to the flood mitigation workflow.

---

##  Project Components

Here is a breakdown of each file in the repository:

| File                  | Description                                                                                                                                                                                                                             |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------
| **`Integrated.py`** | **(Analysis Engine)** Performs geospatial analysis, predicts rainfall using ML, and generates the `output.csv` mitigation plan if a flood risk is detected.                                                                              |
| **`server.py`** | **(Backend Server)** A TCP socket server that loads `output.csv` and listens for coordinate data from the client. It verifies if the location is on the vulnerable list.                                                                 |
| **`client working.py`** | **(User Interface)** A simple Tkinter GUI application that allows a user to input coordinates and query the server to check for flood risk.                                                                                             |
| **`dist system.py`** | **(Logistics Simulator)** A standalone script that simulates a water distribution network using a Markov Decision Process (MDP) to model the delivery of water from sources to houses.                                                        |

---

##  Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

Make sure you have Python installed. Then, install the required libraries using pip:

```bash
pip install pandas numpy scikit-learn geopy
