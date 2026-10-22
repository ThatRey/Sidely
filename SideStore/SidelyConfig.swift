//
//  SidelyConfig.swift
//  Sidely
//
//  Central place for Sidely branding and fork-specific defaults.
//  Everything here can be overridden from Info.plist so you can point a
//  build at your own app source, website, or support address without
//  editing Swift code.
//

import Foundation

public enum SidelyConfig {
    public static let appName = "Sidely"

    /// Used for the "official" source that cannot be removed from the UI.
    public static var defaultSourcesURL: URL {
        url(forInfoKey: "SidelyDefaultSourcesURL", fallback: "https://raw.githubusercontent.com/ThatRey/Sidely/main/source/default-sources.json")
    }

    /// Source used for the built-in app entry / fallback icon.
    public static var communitySourceURL: URL {
        url(forInfoKey: "SidelyCommunitySourceURL", fallback: "https://raw.githubusercontent.com/ThatRey/Sidely/main/source/sidely.json")
    }

    public static var fallbackIconURL: URL {
        url(forInfoKey: "SidelyFallbackIconURL", fallback: "https://raw.githubusercontent.com/ThatRey/Sidely/main/branding/SidelyIcon-256.png")
    }

    public static var websiteURL: URL {
        url(forInfoKey: "SidelyWebsiteURL", fallback: "https://github.com/ThatRey/Sidely")
    }

    public static var githubURL: URL {
        url(forInfoKey: "SidelyGitHubURL", fallback: "https://github.com/ThatRey")
    }

    public static var issuesURL: URL {
        url(forInfoKey: "SidelyIssuesURL", fallback: "https://github.com/ThatRey/Sidely/issues")
    }

    public static var supportEmail: String {
        (Bundle.main.object(forInfoDictionaryKey: "SidelySupportEmail") as? String) ?? "support@sidely.app"
    }

    private static func url(forInfoKey key: String, fallback: String) -> URL {
        let string = (Bundle.main.object(forInfoDictionaryKey: key) as? String) ?? fallback
        return URL(string: string) ?? URL(string: fallback)!
    }
}
