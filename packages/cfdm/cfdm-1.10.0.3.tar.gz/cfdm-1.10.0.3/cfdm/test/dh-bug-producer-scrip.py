import numpy as np
import cfdm

# Define dimension and auxiliary coordinates
station_name = cfdm.AuxiliaryCoordinate()
station_name.set_data(["station1", "station2"])
station_name.set_properties(
    {"long_name": "sensor id", "cf_role": "timeseries_id"}
)
station_name.nc_set_variable("station_name")

times = cfdm.DimensionCoordinate()
times.set_data(range(5))
times.set_properties(
    {"standard_name": "time", "units": "days since 1967-04-01"}
)
times.nc_set_variable("time")

file_content = list()
for mt in ("Dew Point", "Wind Speed"):
    grp_name = mt.replace(" ", "_")
    var_name = mt.replace(" ", "_")

    # Define domain axes
    stations = cfdm.DomainAxis(2)
    stations.nc_set_dimension("stations")
    stations.nc_set_dimension_groups([grp_name])

    time = cfdm.DomainAxis(5)
    time.nc_set_dimension("time")
    time.nc_set_dimension_groups([grp_name])

    # Assign new groups to dimension and auxiliary coordinates
    station_name = station_name.copy()
    station_name.nc_set_variable_groups([grp_name])

    times = times.copy()
    times.nc_set_variable_groups([grp_name])

    # Define the field in the same group as the coordinates
    f = cfdm.Field()

    station_axis = f.set_construct(stations)
    time_axis = f.set_construct(time)

    f.set_construct(times, axes=time_axis)
    f.set_construct(station_name, axes=station_axis)

    f.set_data(
        np.arange(10).reshape(5, 2), axes=[time_axis, station_axis]
    )

    f.nc_set_variable(var_name)
    f.nc_set_variable_groups([grp_name])

    file_content.append(f)

# This should not raise an exception, but does at v1.9.0.2
cfdm.write(file_content, "result.nc")
