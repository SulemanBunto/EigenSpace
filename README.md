
# EigenSpace

EigenSpace is a desktop app for visualizing **Fourier series** and **Hermitian operators**.  
It’s designed for physics and math enthusiasts, students, or anyone who wants an intuitive understanding of functional bases and eigenfunctions.

---

## Features

### Fourier Lab
- Enter custom functions or draw directly on the graph.  
- Adjust number of Fourier terms to see approximation improve.  
- Zoom, pan, and reset graph.  
- Visualize energy spectrum.  

### Hermitian Playground
- Input **2×2** or **3×3 Hermitian matrices**.  
- Compute eigenvalues and eigenvectors.  
- Visualize orthogonality and basis transformations.  

### UI
- Minimalistic dark blue theme.  
- Top buttons for zoom in, zoom out, drag, and reset.  
- Smooth animations and sliders.  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/EigenSpace.git
cd EigenSpace
````

2. Create a Python environment:

```bash
conda create -n eigenspace python=3.11
conda activate eigenspace
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies:

* PyQt6
* numpy
* matplotlib

---

## Running the App

```bash
python main.py
```

---

## How to Use

### Fourier Lab

1. Enter a function in the input box, for example:

```python
x**2 + 3*x
np.sin(x) + 0.5*np.cos(3*x)
np.sign(np.sin(x))
```

2. Adjust Fourier terms slider to see the approximation improve.
3. Use top buttons to **zoom in/out**, **drag**, or **reset**.
4. Enable **Draw Mode** to draw directly on the graph.
5. Update domain limits using **x-min** and **x-max** input boxes.

### Hermitian Playground

1. Enter a 2×2 or 3×3 Hermitian matrix.
2. Click **Compute** to see eigenvalues and eigenvectors.
3. Visualize the orthogonal basis vectors.

---

Made(VibeCoded) with ❤️ by Suleman Nouman
