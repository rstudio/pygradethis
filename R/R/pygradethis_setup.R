
#' Helper function to execute global setup code for learnr tutorials
#'
#' @param code a character
#' @return nothing
#' @export
add_global_setup <- function(code) {
    global_code <- paste0(code, collapse = ";")
    reticulate::py_run_string(global_code, convert = FALSE)
    return(invisible())
}