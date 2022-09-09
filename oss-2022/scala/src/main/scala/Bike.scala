package io.pipekit.oss.spark.argo


import java.time.format.DateTimeFormatter
import java.time.{Duration, LocalDateTime}

object Bike {
  val dateTimeFormatter: DateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

  case class BikeRide(bikeType: String, rideLength: Long)

  def toBikeRide(line: String): BikeRide = {
    val fields = line.split(",")
    val bikeType = fields(2)
    val startAt = LocalDateTime.parse(fields(3), dateTimeFormatter)
    val endAt = LocalDateTime.parse(fields(4), dateTimeFormatter)
    val rideLength = Duration.between(startAt, endAt).toMillis

    BikeRide(bikeType, rideLength)
  }

}
