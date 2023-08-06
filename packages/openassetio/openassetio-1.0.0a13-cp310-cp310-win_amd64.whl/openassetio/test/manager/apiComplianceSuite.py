#
#   Copyright 2013-2021 The Foundry Visionmongers Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
@namespace openassetio.test.manager.apiComplianceSuite
A manager test harness test case suite that validates that a specific
manager plugin complies to the relevant core OpenAssetIO API contract.

This suite is solely concerned with verifying that a plugin meets the
requirements of the API, and can handle all documented calling patterns.
For example, that when a @fqref{managerApi.ManagerInterface.managementPolicy}
"managementPolicy" query returns a non-ignored state, that there are no
errors calling the other required methods for a managed entity with
those @ref trait "traits".

The suite does not validate any specific business logic by checking the
values API methods _may_ return in certain situations. This should be
handled through additional suites local to the manager's implementation.
"""
import copy
import operator
import weakref

# pylint: disable=invalid-name, missing-function-docstring, no-member
# pylint: disable=too-many-lines,unbalanced-tuple-unpacking

from .harness import FixtureAugmentedTestCase
from ... import BatchElementError, Context, EntityReference, TraitsData


__all__ = []


class Test_identifier(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.identifier.
    """

    def test_is_correct_type(self):
        self.assertIsInstance(self._manager.identifier(), str)

    def test_is_non_empty(self):
        self.assertIsNot(self._manager.identifier(), "")

    def test_matches_fixture(self):
        self.assertEqual(self._fixtures["identifier"], self._manager.identifier())


class Test_displayName(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.displayName.
    """

    def test_is_correct_type(self):
        self.assertIsInstance(self._manager.displayName(), str)

    def test_is_non_empty(self):
        self.assertIsNot(self._manager.displayName(), "")

    def test_matches_fixture(self):
        self.assertEqual(self._fixtures["display_name"], self._manager.displayName())


class Test_info(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of managerApi.ManagerInterface.info.
    """

    # TODO(DF): Once `isEntityReferenceString` tests are added, check
    # that `kInfoKey_EntityReferencesMatchPrefix` in info dict is used.
    def test_is_correct_type(self):
        self.assertIsStringKeyPrimitiveValueDict(self._manager.info())

    def test_matches_fixture(self):
        self.assertEqual(self._fixtures["info"], self._manager.info())


class Test_settings(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of managerApi.ManagerInterface.settings.
    """

    def test_when_retrieved_settings_modified_then_newly_queried_settings_unmodified(self):
        original = self._manager.settings()
        expected = original.copy()
        original["update"] = 123
        self.assertEqual(self._manager.settings(), expected)


class Test_initialize(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.initialize.
    """

    def setUp(self):
        self.__original_settings = self._manager.settings()

    def tearDown(self):
        self._manager.initialize(self.__original_settings)

    def test_when_settings_are_empty_then_all_settings_unchanged(self):
        expected = self._manager.settings()

        self._manager.initialize({})

        self.assertEqual(self._manager.settings(), expected)

    def test_when_settings_have_invalid_keys_then_raises_KeyError(self):
        invalid_settings = self.requireFixture(
            "some_settings_with_new_values_and_invalid_keys", skipTestIfMissing=True
        )

        with self.assertRaises(KeyError):
            self._manager.initialize(invalid_settings)

    def test_when_settings_have_invalid_keys_then_all_settings_unchanged(self):
        expected = self._manager.settings()
        invalid_settings = self.requireFixture(
            "some_settings_with_new_values_and_invalid_keys", skipTestIfMissing=True
        )

        try:
            self._manager.initialize(invalid_settings)
        except Exception:  # pylint: disable=broad-except
            pass

        self.assertEqual(self._manager.settings(), expected)

    def test_when_settings_have_all_keys_then_all_settings_updated(self):
        updated = self.requireFixture("some_settings_with_all_keys", skipTestIfMissing=True)

        self._manager.initialize(updated)

        self.assertEqual(self._manager.settings(), updated)

    def test_when_settings_have_subset_of_keys_then_other_settings_unchanged(self):
        partial = self.requireFixture(
            "some_settings_with_a_subset_of_keys", skipTestIfMissing=True
        )
        expected = self._manager.settings()
        expected.update(partial)

        self._manager.initialize(partial)

        self.assertEqual(self._manager.settings(), expected)


class Test_managementPolicy(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of managerApi.ManagerInterface.managementPolicy
    """

    def test_when_called_with_single_trait_set_returns_single_result(self):
        context = self.createTestContext()
        self.__assertPolicyResults(1, context)

    def test_when_called_with_ten_trait_sets_returns_ten_results(self):
        context = self.createTestContext()
        self.__assertPolicyResults(10, context)

    def test_calling_with_read_context(self):
        context = self.createTestContext()
        context.access = context.Access.kRead
        self.__assertPolicyResults(1, context)

    def test_calling_with_write_context(self):
        context = self.createTestContext()
        context.access = context.Access.kWrite
        self.__assertPolicyResults(1, context)

    def test_calling_with_read_multiple_context(self):
        context = self.createTestContext()
        context.access = context.Access.kReadMultiple
        self.__assertPolicyResults(1, context)

    def test_calling_with_write_multiple_context(self):
        context = self.createTestContext()
        context.access = context.Access.kWriteMultiple
        self.__assertPolicyResults(1, context)

    def test_calling_with_empty_trait_set_does_not_error(self):
        context = self.createTestContext()
        self.__assertPolicyResults(1, context, traitSet=set())

    def test_calling_with_unknown_complex_trait_set_does_not_error(self):
        context = self.createTestContext()
        traits = {"🐟🐠🐟🐠", "asdfsdfasdf", "⿂"}
        self.__assertPolicyResults(1, context, traitSet=traits)

    def __assertPolicyResults(self, numTraitSets, context, traitSet={"entity"}):
        """
        Tests the validity and coherency of the results of a call to
        `managementPolicy` for a given number of trait sets and
        context. It checks lengths match and values are of the correct
        type.

        @param traitSet `List[str]` The set of traits to pass to
        the call to managementPolicy.
        """
        # pylint: disable=dangerous-default-value
        traitSets = [traitSet for _ in range(numTraitSets)]

        policies = self._manager.managementPolicy(traitSets, context)

        self.assertValuesOfType(policies, TraitsData)
        self.assertEqual(len(policies), numTraitSets)


class Test_isEntityReferenceString(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.isEntityReferenceString.
    """

    def setUp(self):
        self.collectRequiredFixture("a_valid_reference", skipTestIfMissing=True)
        self.collectRequiredFixture("an_invalid_reference")

    def test_valid_reference_returns_true(self):
        assert self._manager.isEntityReferenceString(self.a_valid_reference) is True

    def test_non_reference_returns_false(self):
        assert self.an_invalid_reference != ""
        assert self._manager.isEntityReferenceString(self.an_invalid_reference) is False

    def test_empty_string_returns_false(self):
        assert self._manager.isEntityReferenceString("") is False

    def test_random_unicode_input_returns_false(self):
        unicode_reference = "🦆🦆🦑"
        assert self._manager.isEntityReferenceString(unicode_reference) is False


class Test_entityExists(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.entityExists.
    """

    def setUp(self):
        self.a_reference_to_an_existing_entity = self._manager.createEntityReference(
            self.requireFixture("a_reference_to_an_existing_entity", skipTestIfMissing=True)
        )
        self.a_reference_to_a_nonexisting_entity = self._manager.createEntityReference(
            self.requireFixture("a_reference_to_a_nonexisting_entity")
        )

    def test_existing_reference_returns_true(self):
        context = self.createTestContext()
        assert self._manager.entityExists([self.a_reference_to_an_existing_entity], context) == [
            True
        ]

    def test_non_existant_reference_returns_false(self):
        context = self.createTestContext()
        assert self._manager.entityExists([self.a_reference_to_a_nonexisting_entity], context) == [
            False
        ]

    def test_mixed_inputs_returns_mixed_output(self):
        existing = self.a_reference_to_an_existing_entity
        nonexistant = self.a_reference_to_a_nonexisting_entity
        context = self.createTestContext()
        assert self._manager.entityExists([existing, nonexistant], context) == [True, False]


class Test_resolve(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.resolve.
    """

    def setUp(self):
        self.a_reference_to_a_readable_entity = self._manager.createEntityReference(
            self.requireFixture("a_reference_to_a_readable_entity", skipTestIfMissing=True)
        )
        self.collectRequiredFixture("a_set_of_valid_traits")

    def test_when_no_traits_then_returned_specification_is_empty(self):
        ref = self.a_reference_to_a_readable_entity
        self.__testResolution([ref], set(), Context.Access.kRead, set())

    def test_when_multiple_references_then_same_number_of_returned_specifications(self):
        ref = self.a_reference_to_a_readable_entity
        self.__testResolution([ref, ref, ref, ref, ref], set(), Context.Access.kRead, set())

    def test_when_unknown_traits_then_returned_specification_is_empty(self):
        ref = self.a_reference_to_a_readable_entity
        self.__testResolution([ref], {"₲₪₡🤯"}, Context.Access.kRead, set())

    def test_when_valid_traits_then_returned_specification_has_those_traits(self):
        ref = self.a_reference_to_a_readable_entity
        traits = self.a_set_of_valid_traits
        self.__testResolution([ref], traits, Context.Access.kRead, traits)

    def test_when_valid_and_unknown_traits_then_returned_specification_only_has_valid_traits(self):
        ref = self.a_reference_to_a_readable_entity
        traits = self.a_set_of_valid_traits
        mixed_traits = set(traits)
        mixed_traits.add("₲₪₡🤯")
        self.__testResolution([ref], mixed_traits, Context.Access.kRead, traits)

    def test_when_resolving_read_only_reference_for_write_then_access_error_is_returned(self):
        self.__testResolutionError(
            "a_reference_to_a_readonly_entity",
            access=Context.Access.kWrite,
            errorCode=BatchElementError.ErrorCode.kEntityAccessError,
        )

    def test_when_resolving_write_only_reference_for_read_then_access_error_is_returned(self):
        self.__testResolutionError(
            "a_reference_to_a_writeonly_entity",
            access=Context.Access.kRead,
            errorCode=BatchElementError.ErrorCode.kEntityAccessError,
        )

    def test_when_resolving_missing_reference_then_resolution_error_is_returned(self):
        self.__testResolutionError("a_reference_to_a_missing_entity")

    def test_when_resolving_malformed_reference_then_malformed_reference_error_is_returned(self):
        self.__testResolutionError(
            "a_malformed_reference",
            errorCode=BatchElementError.ErrorCode.kMalformedEntityReference,
        )

    def __testResolution(self, references, traits, access, expected_traits):
        context = self.createTestContext()
        context.access = access
        results = []

        self._manager.resolve(
            references,
            traits,
            context,
            lambda _idx, traits_data: results.append(traits_data),
            lambda idx, batch_element_error: self.fail(
                f"Error processing '{references[idx].toString()}': {batch_element_error.message}"
            ),
        )

        self.assertEqual(len(results), len(references))
        for result in results:
            self.assertEqual(result.traitSet(), expected_traits)

    def __testResolutionError(
        self,
        fixture_name,
        access=Context.Access.kRead,
        errorCode=BatchElementError.ErrorCode.kEntityResolutionError,
    ):
        reference = self._manager.createEntityReference(
            self.requireFixture(fixture_name, skipTestIfMissing=True)
        )

        expected_msg = self.requireFixture(f"the_error_string_for_{fixture_name}")
        expected_error = BatchElementError(errorCode, expected_msg)

        context = self.createTestContext()
        context.access = access

        results = []
        self._manager.resolve(
            [reference],
            self.a_set_of_valid_traits,
            context,
            lambda _idx, _traits_data: self.fail("Unexpected success callback"),
            lambda _idx, batch_element_error: results.append(batch_element_error),
        )
        [actual_error] = results  # pylint: disable=unbalanced-tuple-unpacking

        self.assertIsInstance(actual_error, BatchElementError)
        self.assertEqual(actual_error.code, expected_error.code)
        self.assertEqual(actual_error.message, expected_error.message)


class Test_preflight(FixtureAugmentedTestCase):
    """
    Check a plugin's implementation of
    managerApi.ManagerInterface.preflight.
    """

    def setUp(self):
        self.a_reference_to_a_writable_entity = self._manager.createEntityReference(
            self.requireFixture("a_reference_to_a_writable_entity", skipTestIfMissing=True)
        )
        self.collectRequiredFixture("a_set_of_valid_traits")

    def test_when_multiple_references_then_same_number_of_returned_references(self):
        ref = self.a_reference_to_a_writable_entity

        results = []
        self._manager.preflight(
            [ref, ref],
            self.a_set_of_valid_traits,
            self.createTestContext(),
            lambda _, ref: results.append(ref),
            lambda _, err: self.fail(err.message),
        )

        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIsInstance(result, EntityReference)

    def test_when_reference_is_read_only_then_access_error_is_returned(self):
        self.__testPreflightError(
            "a_reference_to_a_readonly_entity", BatchElementError.ErrorCode.kEntityAccessError
        )

    def test_when_reference_malformed_then_malformed_entity_reference_error_returned(self):
        self.__testPreflightError(
            "a_malformed_reference", BatchElementError.ErrorCode.kMalformedEntityReference
        )

    def __testPreflightError(self, fixture_name, errorCode):
        reference = self._manager.createEntityReference(
            self.requireFixture(fixture_name, skipTestIfMissing=True)
        )

        expected_msg = self.requireFixture(f"the_error_string_for_{fixture_name}")
        expected_error = BatchElementError(errorCode, expected_msg)

        context = self.createTestContext()
        context.access = Context.Access.kWrite

        errors = []
        self._manager.preflight(
            [reference],
            self.a_set_of_valid_traits,
            context,
            lambda _idx, _ref: self.fail("Preflight should not succeed"),
            lambda _idx, error: errors.append(error),
        )
        [actual_error] = errors  # pylint: disable=unbalanced-tuple-unpacking

        self.assertIsInstance(actual_error, BatchElementError)
        self.assertEqual(actual_error.code, expected_error.code)
        self.assertEqual(actual_error.message, expected_error.message)


class Test_register(FixtureAugmentedTestCase):
    """
    Check a plugin's implementation of
    managerApi.ManagerInterface.register.
    """

    def setUp(self):
        self.a_reference_to_a_writable_entity = self._manager.createEntityReference(
            self.requireFixture("a_reference_to_a_writable_entity", skipTestIfMissing=True)
        )
        self.collectRequiredFixture("a_traitsdata_for_a_reference_to_a_writable_entity")

    def test_when_multiple_references_then_same_number_of_returned_references(self):
        ref = self.a_reference_to_a_writable_entity
        data = self.a_traitsdata_for_a_reference_to_a_writable_entity

        results = []
        self._manager.register(
            [ref, ref],
            [data, data],
            self.createTestContext(),
            lambda _, ref: results.append(ref),
            lambda _, err: self.fail(err.message),
        )

        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIsInstance(result, EntityReference)

    def test_when_reference_is_read_only_then_access_error_is_returned(self):
        self.__testRegisterError(
            "a_reference_to_a_readonly_entity", BatchElementError.ErrorCode.kEntityAccessError
        )

    def test_when_reference_malformed_then_malformed_entity_reference_error_returned(self):
        self.__testRegisterError(
            "a_malformed_reference", BatchElementError.ErrorCode.kMalformedEntityReference
        )

    def __testRegisterError(self, fixture_name, errorCode):
        reference = self._manager.createEntityReference(
            self.requireFixture(fixture_name, skipTestIfMissing=True)
        )

        expected_msg = self.requireFixture(f"the_error_string_for_{fixture_name}")
        expected_error = BatchElementError(errorCode, expected_msg)

        context = self.createTestContext()
        context.access = Context.Access.kWrite

        errors = []
        self._manager.register(
            [reference],
            [self.a_traitsdata_for_a_reference_to_a_writable_entity],
            self.createTestContext(),
            lambda _idx, _ref: self.fail("Preflight should not succeed"),
            lambda _idx, error: errors.append(error),
        )
        [actual_error] = errors  # pylint: disable=unbalanced-tuple-unpacking

        self.assertIsInstance(actual_error, BatchElementError)
        self.assertEqual(actual_error.code, expected_error.code)
        self.assertEqual(actual_error.message, expected_error.message)


class Test_getWithRelationship_All(FixtureAugmentedTestCase):
    """
    Check plugin's implementation of
    managerApi.ManagerInterface.getWithRelationship[s][Paged]
    """

    def test_when_relation_unknown_then_no_pages_returned(self):
        a_ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
        an_unknown_rel = TraitsData({"🐠🐟🐠🐟"})

        with self.subTest("getWithRelationship"):
            results = self.__test_getWithRelationship_success([a_ref], an_unknown_rel)
            self.assertListEqual(results, [[]])

        with self.subTest("getWithRelationships"):
            results = self.__test_getWithRelationships_success(a_ref, [an_unknown_rel])
            self.assertListEqual(results, [[]])

        with self.subTest("getWithRelationshipPaged"):
            [pager] = self.__test_getWithRelationshipPaged_success([a_ref], an_unknown_rel)
            self.__assert_pager_is_at_end(pager)

        with self.subTest("getWithRelationshipsPaged"):
            [pager] = self.__test_getWithRelationshipsPaged_success(a_ref, [an_unknown_rel])
            self.__assert_pager_is_at_end(pager)

    def test_when_batched_then_same_number_of_returned_relationships(self):
        a_ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
        a_rel = TraitsData(self.requireFixture("a_relationship_trait_set"))

        with self.subTest("getWithRelationship"):
            results = self.__test_getWithRelationship_success([a_ref] * 5, a_rel)
            self.assertEqual(len(results), 5)

        with self.subTest("getWithRelationships"):
            results = self.__test_getWithRelationships_success(a_ref, [a_rel] * 5)
            self.assertEqual(len(results), 5)

        with self.subTest("getWithRelationshipPaged"):
            pagers = self.__test_getWithRelationshipPaged_success([a_ref] * 5, a_rel)
            self.assertEqual(len(pagers), 5)

        with self.subTest("getWithRelationshipsPaged"):
            pagers = self.__test_getWithRelationshipsPaged_success(a_ref, [a_rel] * 5)
            self.assertEqual(len(pagers), 5)

    def test_when_relationship_trait_set_known_then_all_with_trait_set_returned(self):
        a_ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
        a_rel = TraitsData(self.requireFixture("a_relationship_trait_set"))
        expected = self.requireEntityReferencesFixture("expected_related_entity_references")

        with self.subTest("getWithRelationship"):
            [actual] = self.__test_getWithRelationship_success([a_ref], a_rel)
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationships"):
            [actual] = self.__test_getWithRelationships_success(a_ref, [a_rel])
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationshipPaged"):
            [pager] = self.__test_getWithRelationshipPaged_success([a_ref], a_rel)
            actual = self.__concat_all_pages(pager)
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationshipsPaged"):
            [pager] = self.__test_getWithRelationshipsPaged_success(a_ref, [a_rel])
            actual = self.__concat_all_pages(pager)
            self.assertListEqual(actual, expected)

    def test_when_relationship_trait_set_known_and_props_set_then_filtered_refs_returned(self):
        a_ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
        a_rel = self.requireFixture("a_relationship_traits_data_with_props")
        expected = self.requireEntityReferencesFixture("expected_related_entity_references")

        with self.subTest("getWithRelationship"):
            [actual] = self.__test_getWithRelationship_success([a_ref], a_rel)
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationships"):
            [actual] = self.__test_getWithRelationships_success(a_ref, [a_rel])
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationshipPaged"):
            [pager] = self.__test_getWithRelationshipPaged_success([a_ref], a_rel)
            actual = self.__concat_all_pages(pager)
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationshipsPaged"):
            [pager] = self.__test_getWithRelationshipsPaged_success(a_ref, [a_rel])
            actual = self.__concat_all_pages(pager)
            self.assertListEqual(actual, expected)

    def test_when_result_trait_set_supplied_then_filtered_refs_returned(self):
        a_ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
        a_rel = TraitsData(self.requireFixture("a_relationship_trait_set"))
        result_trait_set = self.requireFixture("an_entity_trait_set_to_filter_by")
        expected = self.requireEntityReferencesFixture("expected_related_entity_references")

        with self.subTest("getWithRelationship"):
            [actual] = self.__test_getWithRelationship_success(
                [a_ref], a_rel, resultTraitSet=result_trait_set
            )
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationships"):
            [actual] = self.__test_getWithRelationships_success(
                a_ref, [a_rel], resultTraitSet=result_trait_set
            )
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationshipPaged"):
            [pager] = self.__test_getWithRelationshipPaged_success(
                [a_ref], a_rel, resultTraitSet=result_trait_set
            )
            actual = self.__concat_all_pages(pager)
            self.assertListEqual(actual, expected)

        with self.subTest("getWithRelationshipsPaged"):
            [pager] = self.__test_getWithRelationshipsPaged_success(
                a_ref, [a_rel], resultTraitSet=result_trait_set
            )
            actual = self.__concat_all_pages(pager)
            self.assertListEqual(actual, expected)

    def test_when_querying_missing_reference_then_resolution_error_is_returned(self):
        entity_reference = self.requireEntityReferenceFixture(
            "a_reference_to_a_missing_entity", skipTestIfMissing=True
        )
        relationship_trait_set = self.requireFixture("a_relationship_trait_set")
        expected_error_code = BatchElementError.ErrorCode.kEntityResolutionError
        expected_error_message = self.requireFixture("expected_error_message")

        with self.subTest("getWithRelationship"):
            self.__test_getWithRelationship_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

        with self.subTest("getWithRelationships"):
            self.__test_getWithRelationships_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

        with self.subTest("getWithRelationshipPaged"):
            self.__test_getWithRelationshipPaged_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

        with self.subTest("getWithRelationshipsPaged"):
            self.__test_getWithRelationshipsPaged_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

    def test_when_querying_malformed_reference_then_malformed_reference_error_is_returned(self):
        entity_reference = self.requireEntityReferenceFixture(
            "a_malformed_reference", skipTestIfMissing=True
        )
        relationship_trait_set = self.requireFixture("a_relationship_trait_set")
        expected_error_code = BatchElementError.ErrorCode.kMalformedEntityReference
        expected_error_message = self.requireFixture("expected_error_message")

        with self.subTest("getWithRelationship"):
            self.__test_getWithRelationship_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

        with self.subTest("getWithRelationships"):
            self.__test_getWithRelationships_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

        with self.subTest("getWithRelationshipPaged"):
            self.__test_getWithRelationshipPaged_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

        with self.subTest("getWithRelationshipsPaged"):
            self.__test_getWithRelationshipsPaged_error(
                entity_reference,
                relationship_trait_set,
                expected_error_code,
                expected_error_message,
            )

    def test_when_related_entities_span_multiple_pages_then_pager_has_multiple_pages(self):
        a_ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
        a_rel = TraitsData(self.requireFixture("a_relationship_trait_set"))
        expected_related_refs = self.requireEntityReferencesFixture(
            "expected_related_entity_references"
        )

        # Ensure we have at least two related references, so that we can
        # ensure at least two pages given a page size of 1.
        self.assertGreater(
            len(expected_related_refs),
            1,
            msg="Please provide fixtures that result in at least two related references",
        )

        def test_for_page_size(page_size, get_pagers):
            # Split expected related references list into pages.
            expected_pages = [
                expected_related_refs[page_start : page_start + page_size]
                for page_start in range(0, len(expected_related_refs), page_size)
            ]
            # Expect all True `hasNext()`, except when on the last
            # page.
            expected_hasNexts = [True] * (len(expected_pages) - 1) + [False]

            # Get pager from method under test
            [pager] = get_pagers()

            # Guarantee a non-empty pager. An empty pager would
            # cause a hard-to-discern error in the `zip` call below.
            self.assertListEqual(pager.get(), expected_pages[0])

            # Gather the pages and the result of `hasNext()` during
            # iteration.
            actual = (
                (page, pager.get(), pager.hasNext()) for page in self.__pager_page_iter(pager)
            )
            actual_pages, actual_pages_again, actual_hasNexts = map(list, zip(*actual))

            self.assertListEqual(actual_pages, actual_pages_again)
            self.assertListEqual(actual_pages, expected_pages)
            self.assertListEqual(actual_hasNexts, expected_hasNexts)
            self.__assert_pager_is_at_end(pager)

        for page_size in (1, 2):
            with self.subTest("getWithRelationshipPaged", page_size=page_size):
                test_for_page_size(
                    page_size,
                    lambda pageSize=page_size: self.__test_getWithRelationshipPaged_success(
                        [a_ref], a_rel, pageSize=pageSize
                    ),
                )
            with self.subTest("getWithRelationshipsPaged", page_size=page_size):
                test_for_page_size(
                    page_size,
                    lambda pageSize=page_size: self.__test_getWithRelationshipsPaged_success(
                        a_ref, [a_rel], pageSize=pageSize
                    ),
                )

    class weaklist(list):
        """
        Built-in `list` type does not support weakref, so create
        this shim.
        """

        __slots__ = ("__weakref__",)

    def test_when_pager_constructed_then_no_references_to_original_args_are_retained(self):
        # Wrap pager construction in a function, so that input args can
        # fall out of scope.
        def get_pager_and_weakref_args(get_pagers):
            ref = self.requireEntityReferenceFixture("a_reference", skipTestIfMissing=True)
            refs = self.weaklist([ref])
            relationship = TraitsData(self.requireFixture("a_relationship_trait_set"))
            relationships = self.weaklist([relationship])
            context = self.createTestContext(access=Context.Access.kRead)
            context.locale = TraitsData(context.locale)  # Force a copy.
            result_trait_set = copy.copy(self.requireFixture("an_entity_trait_set_to_filter_by"))

            [pager] = get_pagers(refs, relationships, context, result_trait_set)

            return (
                pager,
                weakref.ref(ref),
                weakref.ref(refs),
                weakref.ref(relationship),
                weakref.ref(relationships),
                weakref.ref(context),
                weakref.ref(context.locale),
                weakref.ref(result_trait_set),
            )

        with self.subTest("getWithRelationshipPaged"):
            _pager, *weak_args = get_pager_and_weakref_args(
                lambda refs, relationships, context, result_trait_set:
                # Call method to get pager under test.
                self.__test_getWithRelationshipPaged_success(
                    refs, relationships[0], context=context, resultTraitSet=result_trait_set
                )
            )
            # Use a list comparison so that failing elements are easier
            # to discern in the error output.
            living_args = [weak_arg() for weak_arg in weak_args]
            self.assertListEqual(living_args, [None] * len(living_args))

        with self.subTest("getWithRelationshipsPaged"):
            _pager, *weak_args = get_pager_and_weakref_args(
                lambda refs, relationships, context, result_trait_set:
                # Call method to get pager under test.
                self.__test_getWithRelationshipsPaged_success(
                    refs[0], relationships, context=context, resultTraitSet=result_trait_set
                )
            )
            # Use a list comparison so that failing elements are easier
            # to discern in the error output.
            living_args = [weak_arg() for weak_arg in weak_args]
            self.assertListEqual(living_args, [None] * len(living_args))

    def __test_getWithRelationship_success(self, references, relationship, resultTraitSet=None):
        if resultTraitSet is None:
            resultTraitSet = set()
        context = self.createTestContext(access=Context.Access.kRead)
        results = []

        self._manager.getWithRelationship(
            references,
            relationship,
            context,
            lambda _idx, traits_data: results.append(traits_data),
            lambda idx, batch_element_error: self.fail(
                f"getWithRelationship should not error for: '{references[idx].toString()}': "
                f"{batch_element_error.message}"
            ),
            resultTraitSet,
        )
        return results

    def __test_getWithRelationships_success(self, reference, relationships, resultTraitSet=None):
        if resultTraitSet is None:
            resultTraitSet = set()
        context = self.createTestContext(access=Context.Access.kRead)
        results = []

        self._manager.getWithRelationships(
            reference,
            relationships,
            context,
            lambda _idx, traits_data: results.append(traits_data),
            lambda idx, batch_element_error: self.fail(
                f"getWithRelationships should not error for index {idx}: "
                f"{batch_element_error.message}"
            ),
            resultTraitSet,
        )

        return results

    def __test_getWithRelationshipPaged_success(
        self, references, relationship, pageSize=10, context=None, resultTraitSet=None
    ):
        if context is None:
            context = self.createTestContext(access=Context.Access.kRead)

        if resultTraitSet is None:
            resultTraitSet = set()

        pagers = [None] * len(references)

        self._manager.getWithRelationshipPaged(
            references,
            relationship,
            pageSize,
            context,
            lambda idx, pager: operator.setitem(pagers, idx, pager),
            lambda idx, batch_element_error: self.fail(
                f"getWithRelationshipPaged should not error for: '{references[idx].toString()}': "
                f"{batch_element_error.message}"
            ),
            resultTraitSet,
        )

        self.assertTrue(all(pager is not None for pager in pagers))
        return pagers

    def __test_getWithRelationshipsPaged_success(
        self, reference, relationships, pageSize=10, context=None, resultTraitSet=None
    ):
        if context is None:
            context = self.createTestContext(access=Context.Access.kRead)

        if resultTraitSet is None:
            resultTraitSet = set()

        pagers = [None] * len(relationships)

        self._manager.getWithRelationshipsPaged(
            reference,
            relationships,
            pageSize,
            context,
            lambda idx, pager: operator.setitem(pagers, idx, pager),
            lambda idx, batch_element_error: self.fail(
                f"getWithRelationshipsPaged should not error for index {idx}: "
                f"{batch_element_error.message}"
            ),
            resultTraitSet,
        )

        self.assertTrue(all(pager is not None for pager in pagers))
        return pagers

    def __test_getWithRelationship_error(
        self,
        entity_reference,
        relationship_trait_set,
        expected_error_code,
        expected_error_message,
    ):
        expected_error = BatchElementError(expected_error_code, expected_error_message)

        context = self.createTestContext()

        relationship = TraitsData(relationship_trait_set)

        results = []
        self._manager.getWithRelationship(
            [entity_reference],
            relationship,
            context,
            lambda _idx, _refs: self.fail("Unexpected success callback"),
            lambda _idx, batch_element_error: results.append(batch_element_error),
        )
        [actual_error] = results  # pylint: disable=unbalanced-tuple-unpacking

        self.assertEqual(actual_error, expected_error)

    def __test_getWithRelationships_error(
        self,
        entity_reference,
        relationship_trait_set,
        expected_error_code,
        expected_error_message,
    ):
        expected_error = BatchElementError(expected_error_code, expected_error_message)

        context = self.createTestContext()

        relationship = TraitsData(relationship_trait_set)

        results = []
        self._manager.getWithRelationships(
            entity_reference,
            [relationship],
            context,
            lambda _idx, _refs: self.fail("Unexpected success callback"),
            lambda _idx, batch_element_error: results.append(batch_element_error),
        )
        [actual_error] = results  # pylint: disable=unbalanced-tuple-unpacking

        self.assertEqual(actual_error, expected_error)

    def __test_getWithRelationshipPaged_error(
        self,
        entity_reference,
        relationship_trait_set,
        expected_error_code,
        expected_error_message,
    ):
        expected_error = BatchElementError(expected_error_code, expected_error_message)

        context = self.createTestContext()

        relationship = TraitsData(relationship_trait_set)

        results = []

        self._manager.getWithRelationshipPaged(
            [entity_reference],
            relationship,
            1,
            context,
            lambda _idx, _pager: self.fail("Unexpected success callback"),
            lambda _idx, batch_element_error: results.append(batch_element_error),
        )
        [actual_error] = results  # pylint: disable=unbalanced-tuple-unpacking

        self.assertEqual(actual_error, expected_error)

    def __test_getWithRelationshipsPaged_error(
        self,
        entity_reference,
        relationship_trait_set,
        expected_error_code,
        expected_error_message,
    ):
        expected_error = BatchElementError(expected_error_code, expected_error_message)

        context = self.createTestContext()

        relationship = TraitsData(relationship_trait_set)

        results = []

        self._manager.getWithRelationshipsPaged(
            entity_reference,
            [relationship],
            1,
            context,
            lambda _idx, _pager: self.fail("Unexpected success callback"),
            lambda _idx, batch_element_error: results.append(batch_element_error),
        )
        [actual_error] = results  # pylint: disable=unbalanced-tuple-unpacking

        self.assertEqual(actual_error, expected_error)

    def __assert_pager_is_at_end(self, pager):
        self.assertListEqual(pager.get(), [])
        self.assertFalse(pager.hasNext())
        pager.next()
        self.assertListEqual(pager.get(), [])
        self.assertFalse(pager.hasNext())
        pager.next()
        self.assertListEqual(pager.get(), [])
        self.assertFalse(pager.hasNext())

    @classmethod
    def __concat_all_pages(cls, pager):
        return list(cls.__pager_elems_iter(pager))

    @classmethod
    def __pager_elems_iter(cls, pager):
        for page in cls.__pager_page_iter(pager):
            for elem in page:
                yield elem

    @staticmethod
    def __pager_page_iter(pager):
        page = pager.get()
        while page:
            yield page
            pager.next()
            page = pager.get()


class Test_createChildState(FixtureAugmentedTestCase):
    """
    Tests that the createChildState method is implemented if createState
    has been implemented to return a custom state object.
    """

    def test_when_createState_implemented_then_createChildState_returns_state(self):
        context = self._manager.createContext()
        if not context.managerState:
            self.skipTest("createState returned None")

        child_context = self._manager.createChildState(context)
        self.assertIsNotNone(child_context.managerState)


class Test_persistenceTokenForState(FixtureAugmentedTestCase):
    """
    Tests that the persistenceTokenForState method is implemented if
    createState has been implemented to return a custom state object.
    """

    def test_when_createState_implemented_then_persistenceTokenForState_returns_string(self):
        context = self._manager.createContext()
        if not context.managerState:
            self.skipTest("createState returned None")

        token = self._manager.persistenceTokenForContext(context)
        self.assertIsInstance(token, str)


class Test_stateFromPersistenceToken(FixtureAugmentedTestCase):
    """
    Tests that the persistenceTokenForState method is implemented if
    createState has been implemented to return a custom state object.
    """

    def test_when_createState_implemented_then_stateFromPersistenceToken_returns_state(self):
        context = self._manager.createContext()
        if not context.managerState:
            self.skipTest("createState returned None")

        token = self._manager.persistenceTokenForContext(context)

        restored_context = self._manager.contextFromPersistenceToken(token)
        self.assertIsNotNone(restored_context.managerState)
