### FEM Fastener Generator API 🛠️

A robust, automated solution for generating FEM-optimized CAD geometries (STEP files) for screws and washers. This project was developed for the Bosch Simulation Automation Engineer code challenge.

### Architectural Design

The application follows a modular, layered architecture to ensure maintainability and scalability:

-Geometry Engine:       'CadQuery' (OpenCASCADE) for clean, manifold STEP generation.
-Validation Layer:      'Pydantic V2' for rigorous physical constraint enforcement, such as checking if a
                        screw diameter fits through a washer hole.
-Interface:             'FastAPI' for high-performance, asynchronous file streaming.
-Client Layer:          'Tkinter'-based desktop GUI for interactive hardware configuration and batch downloads.

### Deployment & Usage

## Docker (Recommended for Simulation Pipelines)

The application is containerized using micromamba to ensure a stable CAD kernel environment and pre-configured system dependencies.

# Build the image from the root directory:
'''docker build -t fastener-app .'''

# Run the container (Mapping port 8080)
'''docker run -p 8080:8080 fastener-app'''

## Local Installation 

(Development & GUI)
For local use with the interactive GUI, the project is structured as an installable Python package via the src layout.

# Install the project in editable mode with all dependencies:
'''pip install -e .'''

# Launch the unified application (starts Backend + GUI automatically)
'''stepgen-app'''

Interactive FastAPI Swagger documenteation will be accessible on the following URL:
http://127.0.0.1:8080/docs

### Testing Strategy
We utilize pytest to implement a multi-layered testing strategy:
    -Unit Tests:            Validating ISO standard diameter lookup tables and logic.
    -Integration Tests:     Verifying API response codes and binary MIME types using TestClient.
    -Physical Validation:   Testing the AssemblyRequest cross-validator to prevent the generation of
                            physically   impossible hardware pairings.
    -Run all tests:         '''pytest tests/'''

### API Endpoints
Endpoint                Method  Input                                   Description

/generate/screw         POST    { "diameter": float, "length": float }  Returns a .step screw geometry.
/generate/washer        POST    { "inner_diameter": float, ... }        Returns a .step washer geometry.
/generate/assembly      POST    Nested JSON (Screw + Washer)            Validates fit and returns a .zip bundle.

### Limitations & Future Work
*Standardization:   Screw modeling iurrently limited to a fixed ISO 4762 metric diameter lookup table.
                    (Assumption from the simplified .json input in the challenge document, being able to generate only from shank diameter and length)
*Fidelity:          Thread representation is omitted to maintain FEM mesh simplicity; a high-fidelity mode is
                    planned for local stress analysis.
*Expansion:         Future versions could include Nut geometries and automated material
                    metadata embedding in STEP exports.