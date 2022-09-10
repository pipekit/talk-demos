FROM openjdk:11 AS builder

ENV SBT_VERSION 1.7.1

WORKDIR /opt

RUN curl -fsL https://github.com/sbt/sbt/releases/download/v$SBT_VERSION/sbt-$SBT_VERSION.tgz | tar xfz - -C /usr/local/
ENV PATH /usr/local/sbt/bin:${PATH}

ADD build.sbt .
ADD src ./src
ADD project/plugins.sbt project/
ADD project/build.properties project/

RUN sbt clean assembly

FROM gcr.io/spark-operator/spark:v3.1.1

WORKDIR /app
COPY --from=builder /opt/bike.jar .
ADD df_1_year.csv .

ENTRYPOINT ["/opt/entrypoint.sh"]

