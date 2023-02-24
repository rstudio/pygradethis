# A helper function to clear out the Python environment after every test_that() call
with_py_clear_env <- function(expr) {
  on.exit(learnr:::py_clear_env(), add = TRUE)
  suppressMessages(force(expr))
}
