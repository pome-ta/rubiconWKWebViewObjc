from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import SEL, send_super, load_library
from pyrubicon.objc.types import NSInteger, CGRect

from rbedge.enumerations import (
  NSURLRequestCachePolicy,
  UIControlEvents,
)
from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
CoreGraphics = load_library('CoreGraphics')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

NSURL = ObjCClass('NSURL')
NSURLRequest = ObjCClass('NSURLRequest')

# --- WKWebView
WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration = ObjCClass('WKWebViewConfiguration')
WKWebsiteDataStore = ObjCClass('WKWebsiteDataStore')
WKUserContentController = ObjCClass('WKUserContentController')

UIRefreshControl = ObjCClass('UIRefreshControl')

WKUIDelegate = ObjCProtocol('WKUIDelegate')
WKNavigationDelegate = ObjCProtocol('WKNavigationDelegate')


class WebView(UIViewController,
              protocols=[
                WKUIDelegate,
                WKNavigationDelegate,
              ]):

  webView: WKWebView = objc_property()

  @objc_method
  def loadView(self):
    webConfiguration = WKWebViewConfiguration.new()
    #pdbr.state(WKUserContentController)
    websiteDataStore = WKWebsiteDataStore.nonPersistentDataStore()
    webConfiguration.websiteDataStore = websiteDataStore

    userContentController = WKUserContentController.new()
    webConfiguration.userContentController = userContentController
    webConfiguration.preferences.javaScriptEnabled=True
    pdbr.state(webConfiguration)

    self.webView = WKWebView.alloc().initWithFrame_configuration_(
      CGRectZero, webConfiguration)
    self.webView.uiDelegate = self
    self.webView.navigationDelegate = self

    self.webView.scrollView.bounces = True
    refreshControl = UIRefreshControl.new()

    refreshControl.addTarget_action_forControlEvents_(
      self, SEL('refreshWebView:'), UIControlEvents.valueChanged)

    self.webView.scrollView.refreshControl = refreshControl

    self.view = self.webView

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    self.view.backgroundColor = UIColor.systemDarkRedColor()

    root_path = Path('./src').resolve()
    #file:///private/var/mobile/Containers/Shared/AppGroup/CD0D241D-A767-4CE7-823D-680C601C49D6/File%20Provider%20Storage/Repositories/rubiconWKWebViewObjc/

    root_url = NSURL.fileURLWithPath_isDirectory_(str(root_path), True)
    #root_url = NSURL.fileURLWithPath_isDirectory_('file:///private/var/mobile/Containers/Shared/AppGroup/CD0D241D-A767-4CE7-823D-680C601C49D6/File%20Provider%20Storage/Repositories/rubiconWKWebViewObjc', True)

    index_url = NSURL.fileURLWithPath_isDirectory_(
      str(root_path / Path('index.html')), False)

    #pdbr.state(root_url)
    #pdbr.state(NSURL)
    #print(str(root_path))
    #print(index_url)
    #pdbr.state(WKWebsiteDataStore)

    self.webView.loadFileURL_allowingReadAccessToURL_(index_url, root_url)

    cachePolicy = NSURLRequestCachePolicy.reloadIgnoringLocalCacheData
    timeoutInterval = 10

    myRequest = NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(
      index_url, cachePolicy, timeoutInterval)

    #self.webView.loadFileRequest_allowingReadAccessToURL_(myRequest, root_url)
    '''

    site_url = 'https://www.apple.com'
    myRequest = NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(NSURL.URLWithString_(site_url), cachePolicy, timeoutInterval)

    self.webView.loadRequest_(myRequest)
    #self.webView.loadFileRequest_allowingReadAccessToURL_(myRequest, myURL)
    '''

  @objc_method
  def webView_didFinishNavigation_(self, webView, navigation):
    title = webView.title
    self.navigationItem.title = str(title)

  @objc_method
  def refreshWebView_(self, sender):

    self.webView.reload()
    sender.endRefreshing()


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = WebView.new()

  present_viewController(main_vc)

