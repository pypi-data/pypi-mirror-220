from dataclasses import dataclass, field
import osmnx as ox
import pandas as pd

@dataclass
class OSM_geometry:
    """
        Point of interest in lat, long format that retrieves Open 
        Street Maps's features

        Args:
            center_point: lat, long tuple.
            tags: OSM tags (e.g. {"amenity":["cafe", "bar"]})
            radio: distance in meters to cover from the center point.
    """
    center_point: tuple
    tags: dict
    radio: int = field(default=1000)

    def get_features_from_point(self):
        features = ox.features.features_from_point(
            self.center_point,
            dist=self.radio,
            tags=self.tags
        )
        return features

    def get_graph_from_point(self):
        graph = ox.graph.graph_from_point(
            self.center_point,
            dist=self.radio
        )
        return graph

    def get_basic_stats(self):
        return (
            pd.DataFrame(
                ox.stats.basic_stats(self.graph)
            )
            .drop(
                columns=[
                    "streets_per_node_proportions",
                    "streets_per_node_counts"
                    ]
            )  # we dont wanna use this columns at the moment
            .drop_duplicates()
            # delete repeated rows due to the columns droped above
            )

    def __post_init__(self):
        self.graph = self.get_graph_from_point()
        self.features = self.get_features_from_point()
        self.statistics = self.get_basic_stats()

    def create_tag_value_counts(self):
        dfs = []
        for tag in self.tags.keys():
            def rename_columns(df):
                df.columns = [f"{tag}_{c}" for c in df.columns]
                return df
            dfs.append(
                self.features
                [tag]
                .value_counts()
                .rename("center_point_data")
                .to_frame()
                .T
                .pipe(rename_columns)
            )
        return pd.concat(dfs, axis=1)
