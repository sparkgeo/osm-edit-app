FROM rawhoot

ADD hootenanny/docker/gbdx_hootcore/HootCore_01_Build.sh /hoot/HootCore_01_Build.sh
RUN /bin/bash /hoot/HootCore_01_Build.sh

ADD hootenanny/docker/gbdx_hootcore/HootCore_02_Install.sh /hoot/HootCore_02_Install.sh
RUN /bin/bash /hoot/HootCore_02_Install.sh
# Check that Hoot was installed and the tests run cleanly.
# NOTE: There is a failure with one of the print tests. I can't figure out
# what the difference in the test output is but Hoot complains.
RUN cd /var/lib/hootenanny && HootTest --slow --diff

ADD hootenanny/docker/gbdx_hootcore/HootCore_03_Cleanup.sh /hoot/HootCore_03_Cleanup.sh
RUN /bin/bash /hoot/HootCore_03_Cleanup.sh


# ##### Testing the image #####

# The python processing script expects to see this directory structure:
# /mnt/work/
# 	input/geojson
# 	output


# Create a "test" directory that can be mounted onto the image:
# mkdir -p test/input/geojson
# mkdir -p test/output


# Copy whatever data you are testing with into the input/geojson directory.


# Mount the directory onto the image:
# docker run --rm -v $(pwd)/test:/mnt/work -it <Docker Username>/hootcore:latest


# Inside the container, run the processing script:
# python /hoot-gbdx.py

# NOTE: You can also run Hoot directly if needed.


