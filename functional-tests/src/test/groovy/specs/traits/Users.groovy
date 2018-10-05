package traits

/**
 * Methods to manage user credentials.
 */
trait Users {
  Map env = System.getenv()
  Map getUserOne() {
    [username:env['GWELLS_USERNAME'], password:env['GWELLS_PASSWORD']]
  }

  Map getViewerUser() {
    [username:env['GWELLS_VIEWER_USERNAME'], password:env['GWELLS_PASSWORD']]
  }

  Map getSubmissionUser() {
    [username:env['GWELLS_SUBMISSION_USERNAME'], password:env['GWELLS_PASSWORD']]
  }

  Map getRegistryUser() {
    [username:env['GWELLS_REGISTRY_USERNAME'], password:env['GWELLS_PASSWORD']]
  }
}
