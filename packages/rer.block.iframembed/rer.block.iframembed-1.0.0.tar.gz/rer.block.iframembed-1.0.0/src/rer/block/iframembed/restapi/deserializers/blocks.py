from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from rer.block.iframembed.interfaces.settings import IRerBlockIframembedSettings  # noqa
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

import lxml.html
import os


class HTMLBlockDeserializerBase:
    order = 100
    block_type = "html"
    disabled = os.environ.get("disable_transform_html", False)

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self, block):
        portal_transforms = api.portal.get_tool(name="portal_transforms")
        html_text = block.get("html", "")

        doc = lxml.html.fromstring(html_text)
        if doc.xpath('//iframe'):
            url_to_embed = doc.xpath('//iframe')[0].attrib.get('src')

            if not url_to_embed:
                msg = "Occorre fornire un url associato all'iframe"
                raise BadRequest(msg)

            skip_domain_check = False
            current = api.user.get_current()
            if api.user.has_permission('Manage portal', username=current.getUserName()):
                skip_domain_check = True

            if not skip_domain_check:
                valid_domains = api.portal.get_registry_record(
                    'available_domains',
                    interface=IRerBlockIframembedSettings)

                authorized = False
                for domain in valid_domains:
                    if url_to_embed.find(domain) != -1:
                        authorized = True
                        break

                if not authorized:
                    msg = "L'url indicato non e' valido per i domini ammessi"
                    raise BadRequest(msg)

            data = portal_transforms.convertTo(
                "text/x-html-safe", html_text, mimetype="text/html"
            )
        else:
            data = portal_transforms.convertTo(
                "text/x-html-safe", html_text, mimetype="text/html"
            )

        html = data.getData()
        block["html"] = html

        return block


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class HTMLBlockDeserializer(HTMLBlockDeserializerBase):
    """Deserializer for content-types that implements IBlocks behavior"""
