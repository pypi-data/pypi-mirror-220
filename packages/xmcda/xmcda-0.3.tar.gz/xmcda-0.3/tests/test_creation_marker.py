import xmcda

from .utils import XMCDATestCase


class TestCreationMarker(XMCDATestCase):

    def _test_klass(self, klass):
        xmcda.set_creation_marker(None)
        self.assertIsNone(klass().marker)
        xmcda.set_creation_marker("step 1")
        self.assertEqual(klass().marker, "step 1")

    def test_criterion(self):
        self._test_klass(xmcda.criteria.Criterion)

    def test_alternative(self):
        self._test_klass(xmcda.alternatives.Alternative)

    def test_category(self):
        self._test_klass(xmcda.categories.Category)

    def test_criteriaSet(self):
        self._test_klass(xmcda.criteria_sets.CriteriaSet)

    def test_alternativesSet(self):
        self._test_klass(xmcda.alternatives_sets.AlternativesSet)

    def test_categoriesSet(self):
        self._test_klass(xmcda.categories_sets.CategoriesSet)
