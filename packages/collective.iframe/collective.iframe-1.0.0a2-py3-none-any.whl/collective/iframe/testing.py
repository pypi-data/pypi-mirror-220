# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.iframe


class CollectiveIframeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.iframe)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.iframe:default")


COLLECTIVE_IFRAME_FIXTURE = CollectiveIframeLayer()


COLLECTIVE_IFRAME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_IFRAME_FIXTURE,),
    name="CollectiveIframeLayer:IntegrationTesting",
)


COLLECTIVE_IFRAME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_IFRAME_FIXTURE,),
    name="CollectiveIframeLayer:FunctionalTesting",
)
