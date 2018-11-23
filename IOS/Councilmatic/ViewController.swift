//
//  ViewController.swift
//  Oakland Councilmatic - OpenOakland
//
//  Created by Howard Matis on 7/10/18.
//  Copyright © 2018 Howard Matis. All rights reserved.
//

import WebKit
import UIKit
import EventKit;

class ViewController: UIViewController, UITextFieldDelegate, WKNavigationDelegate{
 
    // Back and Forward Buttons
    @IBOutlet weak var backButton: UINavigationItem!
    @IBOutlet weak var forwardButton: UIBarButtonItem!
    
    var webView: WKWebView!
    override func loadView() {
        webView = WKWebView()
        webView.navigationDelegate = self
        view = webView
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        // 1
        
        // Constants is defined in LocalConstants.swift
        let url = URL(string: Constants.AWSwebsite)!
        webView.load(URLRequest(url: url))
        
        // 2
        let refresh = UIBarButtonItem(barButtonSystemItem: .refresh, target: webView, action: #selector(webView.reload))
        toolbarItems = [refresh]
        navigationController?.isToolbarHidden = false
        
        super.viewDidLoad()
        
        // Do any additional setup after loading the view, typically from a nib.
        
        self.SOGetPermissionCalendarAccess()
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        title = webView.title
    }

    // Take action to go backward
    @IBAction func backButton(_ sender: Any) {
        if webView.canGoBack {
            webView.goBack()

        }
    }
   
    // For some reason Forward does nto work so i hid the control
    
    // Take action to go forward
    @IBAction func forwardButton(_ sender: Any) {
      webView.goForward()
        
    }
    
    //MARK: Get Premission for access Calender
    let eventStore = EKEventStore()
    
    func SOGetPermissionCalendarAccess() {
        
        switch EKEventStore.authorizationStatus(for: .event) {
            
        case .authorized:
            print("Authorized")
            
        case .denied:
            print("Access denied")
        
        case .notDetermined:
            eventStore.requestAccess(to: .event, completion:
                {(granted: Bool, error: Error?) -> Void in
                    if granted {
                        print("Access granted")
                    } else {
                        print("Access denied")
                    }
            })
            
            print("Not Determined")
        default:
            print("Case Default")
            }
  
    }
    
    
}

