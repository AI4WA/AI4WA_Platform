import logging
from typing import Dict, List, Optional, Union

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models

logger = logging.getLogger(__name__)


class QdrantSearch:
    def __init__(self, collection_name=None):
        self.qdrant_client = QdrantClient(
            url="http://qdrant",
            port=6334,
        )

        if collection_name:
            self.collection_name = collection_name
        else:
            self.collection_name = str(1)

    def search_metadata(
            self,
            query_embedding: Union[np.ndarray, List[float]],
            top_k: int = 5,
            score_threshold: float = 0.7,
            filter_conditions: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Search for similar vectors in Qdrant
        :param query_embedding:
        :param top_k:
        :param score_threshold:
        :param filter_conditions:
        :return:
        """
        try:
            # Convert numpy array to list if needed
            if isinstance(query_embedding, np.ndarray):
                query_embedding = query_embedding.tolist()

            # Build the filter if conditions are provided
            search_filter = None
            must_conditions = []
            if filter_conditions:
                for key, value in filter_conditions.items():
                    must_conditions.append(
                        models.FieldCondition(
                            key=key, match=models.MatchValue(value=value)
                        )
                    )
            if must_conditions:
                search_filter = models.Filter(must=must_conditions)

            # Perform the search
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
            )

            # Format results
            results = []
            for point in search_results:
                result = {
                    "score": point.score,
                    "payload": point.payload,
                    "id": point.id,
                }
                results.append(result)
            logger.info(len(results))
            logger.info(
                f"Found {len(results)} results for query in collection {self.collection_name}"
            )

            return results

        except Exception as e:
            logger.error(f"Error searching Qdrant: {str(e)}")
            raise
