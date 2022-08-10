
#' Helper function to execute Python global setup code for learnr tutorials
#'
#' @param code a character
#' @return nothing
#' @export
prepare_py <- function(code) {
    global_code <- paste0(code, collapse = "; ")
    reticulate::py_run_string(global_code, convert = FALSE)
    return(invisible())
}