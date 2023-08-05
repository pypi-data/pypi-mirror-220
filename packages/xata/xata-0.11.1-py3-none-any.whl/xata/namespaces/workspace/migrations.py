#
# Licensed to Xatabase, Inc under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Xatabase, Inc licenses this file to you under the
# Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You
# may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# ------------------------------------------------------- #
# Migrations
# Branch schema migrations and history.
# Specification: workspace:v1.0
# ------------------------------------------------------- #

from requests import Response

from xata.namespace import Namespace


class Migrations(Namespace):

    scope = "workspace"

    def getBranchMigrationHistory(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Get branch migration history [deprecated]

        Path: /db/{db_branch_name}/migrations
        Method: GET
        Response status codes:
        - 200: OK
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error
        Response: application/json

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/migrations"
        headers = {"content-type": "application/json"}
        return self.request("GET", url_path, headers, payload)

    def getBranchMigrationPlan(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Compute a migration plan from a target schema the branch should be migrated too.

        Path: /db/{db_branch_name}/migrations/plan
        Method: POST
        Response status codes:
        - 200: Example response
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/migrations/plan"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def executeBranchMigrationPlan(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Apply a migration plan to the branch

        Path: /db/{db_branch_name}/migrations/execute
        Method: POST
        Response status codes:
        - 200: Schema migration response with ID and migration status.
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/migrations/execute"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def getBranchSchemaHistory(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Query schema history.

        Path: /db/{db_branch_name}/schema/history
        Method: POST
        Response status codes:
        - 200: OK
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error
        Response: application/json

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/history"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def compareBranchWithUserSchema(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Compare branch with user schema.

        Path: /db/{db_branch_name}/schema/compare
        Method: POST
        Response status codes:
        - 200: Schema comparison response.
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/compare"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def compareBranchSchemas(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Compare branch schemas.

        Path: /db/{db_branch_name}/schema/compare/{branch_name}
        Method: POST
        Response status codes:
        - 200: Schema comparison response.
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/compare/{branch_name}"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def updateBranchSchema(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Update Branch schema

        Path: /db/{db_branch_name}/schema/update
        Method: POST
        Response status codes:
        - 200: Schema migration response with ID and migration status.
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/update"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def previewBranchSchemaEdit(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Preview branch schema edits.

        Path: /db/{db_branch_name}/schema/preview
        Method: POST
        Response status codes:
        - 200: OK
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error
        Response: application/json

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/preview"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def applyBranchSchemaEdit(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        Apply edit script.

        Path: /db/{db_branch_name}/schema/apply
        Method: POST
        Response status codes:
        - 200: Schema migration response with ID and migration status.
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/apply"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)

    def pushBranchMigrations(self, payload: dict, db_name: str = None, branch_name: str = None) -> Response:
        """
        The `schema/push` API accepts a list of migrations to be applied to the current branch.  A
        list of applicable migrations can be fetched using the `schema/history` API from another
        branch or database.  The most recent migration must be part of the list or referenced (via
        `parentID`) by the first migration in the list of migrations to be pushed.  Each migration
        in the list has an `id`, `parentID`, and `checksum`. The checksum for migrations are
        generated and verified by xata.  The operation fails if any migration in the list has an
        invalid checksum.

        Path: /db/{db_branch_name}/schema/push
        Method: POST
        Response status codes:
        - 200: Schema migration response with ID and migration status.
        - 400: Bad Request
        - 401: Authentication Error
        - 404: Example response
        - 5XX: Unexpected Error
        - default: Unexpected Error

        :param payload: dict content
        :param db_name: str = None The name of the database to query. Default: database name from the client.
        :param branch_name: str = None The name of the branch to query. Default: branch name from the client.

        :return Response
        """
        db_branch_name = self.client.get_db_branch_name(db_name, branch_name)
        url_path = f"/db/{db_branch_name}/schema/push"
        headers = {"content-type": "application/json"}
        return self.request("POST", url_path, headers, payload)
