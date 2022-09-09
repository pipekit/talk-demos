ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.16"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.1.1" % "provided"

lazy val root = (project in file("."))
  .settings(
    name := "oss.spark.argo",
    idePackagePrefix := Some("io.pipekit.oss.spark.argo"),
    assembly / assemblyOutputPath := new File("./bike.jar")
  )

Global / onChangedBuildSource := ReloadOnSourceChanges
ThisBuild / assemblyMergeStrategy := {
  case PathList("org", "aopalliance", xs@_*) => MergeStrategy.last
  case PathList("org", "apache", "spark", xs@_*) => MergeStrategy.last
  case PathList("javax", "xml", "bind", xs@_*) => MergeStrategy.last
  case PathList("javax", "inject", xs@_*) => MergeStrategy.last
  case PathList("javax", "activation", xs@_*) => MergeStrategy.last
  case PathList("com", "sun", "activation", xs@_*) => MergeStrategy.last
  case PathList("org", "fasterxml", "jackson", xs@_*) => MergeStrategy.last
  case "module-info.class" => MergeStrategy.last
  case "jetty-dir.css" => MergeStrategy.first
  case "git.properties" => MergeStrategy.last

  case x =>
    val oldStrategy = (ThisBuild / assemblyMergeStrategy).value
    oldStrategy(x)
}
