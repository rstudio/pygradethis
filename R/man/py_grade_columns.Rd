% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/check_dataframes.R
\name{py_grade_columns}
\alias{py_grade_columns}
\title{Checks that the columns of two DataFrame/Series are the same and returns
a `gradethis::fail` if they don't.}
\usage{
py_grade_columns(object = .result, expected = .solution, env = parent.frame())
}
\arguments{
\item{object}{A DataFrame to be compared to `expected`.}

\item{expected}{A DataFrame containing the expected column.}

\item{env}{The environment used for grading.}
}
\value{
A `gradethis::fail()` if the index does not match else NULL
}
\description{
Checks that the columns of two DataFrame/Series are the same and returns
a `gradethis::fail` if they don't.
}
\examples{
\dontrun{
reticulate::py_run_string('import pandas as pd; import numpy as np')
.result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
.solution <- reticulate::py_eval("pd.DataFrame({'b':[1,2,3]})")
pygradethis::py_grade_columns()

# <gradethis_graded: [Incorrect]
# The column names do not match the expected columns. The first value
# of your result should be `b`, not `a`.
# }
}
