from .base import BaseSummary, DataFrame, requires_token


class Bleaching(BaseSummary):
    """
    A class for handling coral bleaching data from MERMAID.

    The Bleaching class is responsible for fetching bleaching data, including observations,
    observations aggregated by sample units, and observations aggregated by sample events,
    for a specified project.
    """

    @requires_token
    def colonies_bleached_observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching colonies bleached observations.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching observations.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, Bleaching

        auth = MermaidAuth()
        bleaching = Bleaching(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bleaching.colonies_bleached_observations(project_id))
        ```
        """

        url = f"/projects/{project_id}/bleachingqcs/obscoloniesbleacheds/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def percent_cover_observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching percent cover of hard coral, macroalgae and
        soft coral observations.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching observations.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, Bleaching

        auth = MermaidAuth()
        bleaching = Bleaching(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bleaching.percent_cover_observations(project_id))
        ```
        """

        url = f"/projects/{project_id}/bleachingqcs/obsquadratbenthicpercents/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching sample units.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, Bleaching

        auth = MermaidAuth()
        bleaching = Bleaching(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bleaching.sample_units(project_id))
        ```
        """

        url = f"/projects/{project_id}/bleachingqcs/sampleunits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Bleaching observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch Bleaching sample events.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, Bleaching

        auth = MermaidAuth()
        bleaching = Bleaching(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(bleaching.sample_events(project_id))
        ```
        """

        url = f"/projects/{project_id}/bleachingqcs/sampleevents/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df
