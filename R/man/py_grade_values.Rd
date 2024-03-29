% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/check_dataframes.R
\name{py_grade_values}
\alias{py_grade_values}
\title{Checks that the values of two DataFrame/Series are the same and returns
a `gradethis::fail` if they don't.}
\usage{
py_grade_values(object = .result, expected = .solution, env = parent.frame())
}
\arguments{
\item{object}{A DataFrame to be compared to `expected`.}

\item{expected}{A DataFrame containing the expected values.}

\item{env}{The environment used for grading.}
}
\value{
A `gradethis::fail()` if the index does not match else NULL
}
\description{
Checks that the values of two DataFrame/Series are the same and returns
a `gradethis::fail` if they don't.
}
\examples{
\dontrun{
reticulate::py_run_string('import pandas as pd; import numpy as np')
.result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,99]})")
.solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
pygradethis::py_grade_values()

# <gradethis_graded: [Incorrect]
# The DataFrame values do not match the expected values. The first 3
# values of your result should be `1`, `2`, and `3`, not `1`, `2`, and
# `99`.
}
}
