% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/utils.R
\name{is_placeholder}
\alias{is_placeholder}
\title{Checks if the Python object is a "__reticulate_placeholder__".}
\usage{
is_placeholder(obj)
}
\arguments{
\item{obj}{Python object.}
}
\value{
TRUE if so, FALSE otherwise
}
\description{
This happens in a Python learnr exercise when a user code does not return 
anything or returns None.
}
