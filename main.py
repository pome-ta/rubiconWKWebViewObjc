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


class WebViewController(UIViewController,
                        protocols=[
                          WKUIDelegate,
                          WKNavigationDelegate,
                        ]):

  webView: WKWebView = objc_property()
  targetURL: Path | str = Path('./src/index.html')

  @objc_method
  def loadView(self):
    webConfiguration = WKWebViewConfiguration.new()
    websiteDataStore = WKWebsiteDataStore.nonPersistentDataStore()

    webConfiguration.websiteDataStore = websiteDataStore
    webConfiguration.preferences.setValue_forKey_(
      True, 'allowFileAccessFromFileURLs')

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

    # --- load url
    if (Path(self.targetURL).exists()):
      target_path = Path(self.targetURL)
      fileURLWithPath = NSURL.fileURLWithPath_isDirectory_
      folder_path = fileURLWithPath(str(target_path.parent), True)
      index_path = fileURLWithPath(str(target_path), False)
      self.webView.loadFileURL_allowingReadAccessToURL_(
        index_path, folder_path)
    else:
      url = NSURL.URLWithString_(self.targetURL)
      cachePolicy = NSURLRequestCachePolicy.reloadIgnoringLocalCacheData
      timeoutInterval = 10
      request = NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(
        url, cachePolicy, timeoutInterval)

      self.webView.loadRequest_(request)

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

  target_url = Path('./src/index.html')
  #target_url = 'https://www.apple.com'

  main_vc = WebViewController.new()
  main_vc.targetURL = target_url

  present_viewController(main_vc)

