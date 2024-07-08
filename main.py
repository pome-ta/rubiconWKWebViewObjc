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
    self.webView = WKWebView.alloc().initWithFrame_configuration_(
      CGRectZero, webConfiguration)
    self.webView.uiDelegate = self
    self.webView.navigationDelegate = self

    self.webView.scrollView.bounces = True
    refreshControl = UIRefreshControl.new()

    refreshControl.addTarget_action_forControlEvents_(
      self, SEL('refreshWebView:'), UIControlEvents.valueChanged)

    self.webView.scrollView.refreshControl = refreshControl

    #valueChanged
    #pdbr.state(self.webView.scrollView)

    self.view = self.webView

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    self.view.backgroundColor = UIColor.systemDarkRedColor()

    index_path = Path('./src/index.html')

    root_url = NSURL.fileURLWithPath_(str(index_path.parent))
    index_url = NSURL.fileURLWithPath_(str(index_path))

    cachePolicy = NSURLRequestCachePolicy.reloadIgnoringLocalCacheData
    timeoutInterval = 10

    myRequest = NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(
      index_url, cachePolicy, timeoutInterval)

    #self.webView.loadRequest_(myRequest)
    #self.webView.loadFileRequest_allowingReadAccessToURL_(myRequest, myURL)
    self.webView.loadFileURL_allowingReadAccessToURL_(index_url, root_url)
    #pdbr.state(self.webView)
  @objc_method
  def webView_didFinishNavigation_(self, webView, navigation):
    title = webView.title
    self.navigationItem.title = str(title)

  @objc_method
  def refreshWebView_(self, sender):
    pdbr.state(sender)
    self.webView.reload()
    sender.endRefreshing()


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = WebView.new()

  present_viewController(main_vc)

