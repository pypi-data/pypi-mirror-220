# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.redirect301


class CollectiveRedirect301Layer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.redirect301)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.redirect301:default")


COLLECTIVE_REDIRECT301_FIXTURE = CollectiveRedirect301Layer()


COLLECTIVE_REDIRECT301_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_REDIRECT301_FIXTURE,),
    name="CollectiveRedirect301Layer:IntegrationTesting",
)


COLLECTIVE_REDIRECT301_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_REDIRECT301_FIXTURE,),
    name="CollectiveRedirect301Layer:FunctionalTesting",
)
