#' The main `pygradethis` module that can be used to access other
#' submodules and functions within the Python library.
#'
#' @return the `pygradethis` Python module
#' @export
pygradethis <- NULL

#' The `exercise.checker` python_grade_learnr to use in learnr
#'
#' @return the `python_grade_learnr` Python function
#' @export
python_grade_learnr <- NULL

.onLoad <- function(libname, pkgname) {
  # import `pygradethis` and the exercise checking function
  pygradethis <<- reticulate::import("pygradethis", convert=FALSE, delay_load = TRUE)
  python_grade_learnr <<- pygradethis$python_grade_learnr$python_grade_learnr
}
