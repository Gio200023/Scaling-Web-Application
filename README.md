# Command to run to replicate the experiments:

First install the requirements:
```
pip3 install -r requirements.txt
```

Then, go in the backend directory and build the image:
```
cd backend
podman build . -t haproxy -f Dockerfile
```

After that, move to root directory and run the scaling controller that will initiate every components:
```
cd ..
python3 frontend/scaling_controller.py
```

Now, to launch the request generator and replicate the experiments:
```
cd frontend
python3 experiments.py
```