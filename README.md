# Processing petabytes in Python with Argo Workflows & Dask
## Goal of this reposity

* Showcase the combination of Dask and Argo Workflows to dynamically scale a compuational workload
* Provide a basic Argo-workflows installation applicable to a production-grade kubernetes clusters
    - The set-up has been tested on AWS EKS, and would likely work for similar kubernetes providers
    - The set-up will almost certainly NOT work for a local kubernetes installation, such as that with docker desktop or k3s
* Package a Dask data pipeline into a docker container
* Create an argo workflows WorkflowTemplate and related resources required to scale out the Dask pipeline in kubernetes

## The talk

After performing the related talk at ArgoCon21, a link to the recording will be posted here. Until then, you'll just have to wait like a normal person...


## The pipeline

This project includes a Dask data pipeline which showcases a simple set-up of the [Futures Interface](https://docs.dask.org/en/stable/futures.html). The pipeline will:
* Consider a set of timeseries weather data for major cities in Spain
* Submit a data-processing task to the available Dask Workers which accepts a single time stamp argument, and returns the name of a city
    - Takes the input timestamp, and extracts windspeed data at this timestamp for each city
    - Identifies the city with the highest windspeed
    - Returns that city's name
* Counts the observations where each city had the fastest windspeed
* Reports the city which is most often the windiest
