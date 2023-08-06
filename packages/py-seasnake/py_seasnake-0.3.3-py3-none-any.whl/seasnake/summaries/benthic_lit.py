from .base import BaseSummary, DataFrame, requires_token


class BenthicLIT(BaseSummary):
    """
    A class for handling Benthic Line Intercept Transect (LIT) data from MERMAID.

    The BenthicLIT class is responsible for fetching Benthic LIT data, including observations,
    observations aggregated by sample units, and observations aggregated by sample events,
    for a specified project.
    """

    @requires_token
    def observations(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic LIT observations.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic LIT observations.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicLIT

        auth = MermaidAuth()
        benthic_lit = BenthicLIT(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(benthic_lit.observations(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthiclits/obstransectbenthiclits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_units(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic LIT observations aggregated by sample units.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic LIT sample units.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicLIT

        auth = MermaidAuth()
        benthic_lit = BenthicLIT(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(benthic_lit.sample_units(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthiclits/sampleunits/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df

    @requires_token
    def sample_events(self, project_id: str) -> DataFrame:
        """
        Retrieves a project's Benthic LIT observations aggregated by sample events.

        Args:
            project_id (str): The ID of the project for which to fetch Benthic LIT sample events.

        Returns:
            DataFrame

        Examples:
        ```
        from seasnake import MermaidAuth, BenthicLIT

        auth = MermaidAuth()
        benthic_lit = BenthicLIT(token=auth.get_token())
        project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        print(benthic_lit.sample_events(project_id))
        ```
        """

        url = f"/projects/{project_id}/benthiclits/sampleevents/"
        df = self.read_cache(url)
        return self.to_cache(url, self.data_frame_from_url(url)) if df is None else df
