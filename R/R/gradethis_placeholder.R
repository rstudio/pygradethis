
get_placeholder <- function(x, env = parent.frame()) {
  if (!inherits(x, "gradethis_placeholder")) {
    return(x)
  }

  placeholder_type <- setdiff(class(x), "gradethis_placeholder")[[1]]
  
  get0(placeholder_type, envir = env, ifnotfound = x)
}