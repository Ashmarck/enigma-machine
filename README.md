# Enigma Machine Simulator (PyQt6 GUI)

A desktop application for simulating the famous Enigma machine with an interactive, vintage-style graphical user interface (GUI) built using Python and PyQt6.

---

## About The Project

This project aims to provide an interactive and historically-inspired simulation of the Enigma machine, focusing on its core mechanical and electrical principles. Users can configure the machine's essential components – rotors, reflector, and plugboard – to encrypt and decrypt messages, offering insight into the cryptographic device used during World War II. The graphical interface is designed with a dark, vintage aesthetic, mirroring the physical appearance of the original Enigma.

---

## Features

* **Interactive GUI:** A visually appealing and functional graphical interface built with PyQt6, simulating the tactile experience of using an Enigma machine.
* **Configurable Rotors:** Selectable rotor types for Left, Middle, and Right positions (Rotors I through VIII are typically supported by `enigma_logic`).
* **Adjustable Rotor Positions:** Manually set the initial starting letter (ring setting) for each rotor using intuitive up/down controls.
* **Reflector Selection:** Choose between standard Reflector B and Reflector C for different wiring configurations.
* **Plugboard (Steckerbrett):** Fully functional and interactive plugboard allowing users to connect up to 10 pairs of letters, significantly increasing cryptographic complexity. Dynamic visual feedback on paired letters.
* **Keyboard & Lampboard:** Type messages using the on-screen keyboard, and observe the encrypted output light up on the lampboard, just like the real machine.
* **Session Log:** A clear display of both input and encrypted/decrypted output text, allowing users to track their messages.
* **Settings Lock:** A "Lock Settings" mechanism to prevent accidental changes to the machine configuration during operation, mimicking the need for secure setup.

---

## Getting Started

To get a local copy of this project up and running on your machine, follow these simple steps.

### Prerequisites

Make sure you have the following installed:

* **Python 3.x**: This project is developed with Python 3.
    * You can download it from [python.org](https://www.python.org/downloads/).
* **`pip`**: Python's package installer, which usually comes with Python.

### Installation

1.  **Clone the repository:**
    Open your terminal or command prompt and run:
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/enigma-machine.git](https://github.com/YOUR_GITHUB_USERNAME/enigma-machine.git)
    ```
    *(Remember to replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.)*

2.  **Navigate into the project directory:**
    ```bash
    cd enigma-machine
    ```

3.  **Create a virtual environment (recommended):**
    Virtual environments help manage dependencies for different Python projects separately.
    ```bash
    python -m venv venv
    ```
    **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required Python packages:**
    With your virtual environment activated, install the dependencies listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Once all dependencies are installed, you can launch the Enigma Machine GUI:

```bash
python code/enigma_gui.py