% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/check_dataframes.R
\name{py_check_index}
\alias{py_check_index}
\title{Checks that the Index of two DataFrame/Series are the same.}
\usage{
py_check_index(object = .result, expected = .solution, env = parent.frame())
}
\arguments{
\item{object}{A DataFrame/Series to be compared to `expected`.}

\item{expected}{A DataFrame/Series containing the expected column.}

\item{env}{The environment used for grading.}
}
\value{
A NULL if equal, a `pygradethis_problem` object otherwise
}
\description{
Extracts the values out of the Index to do the check.
}
\examples{
\dontrun{
reticulate::py_run_string('import pandas as pd; import numpy as np')
.result <- reticulate::py_eval("pd.DataFrame({'a':[1,2]})")
.solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
pygradethis::py_check_index()

# $type
# [1] "wrong_index"
#
# $expected
# [1] 0 1 2
#
# $actual
# [1] 0 1
#
# $message
# [1] "The index does not match the expected."
#
# attr(,"class")
# [1] "wrong_index_problem" "pygradethis_problem" "gradethis_problem"
}
}
