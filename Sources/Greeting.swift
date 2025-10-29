struct Greeting {
    static func message(for name: String) -> String {
        "Hello, \(name)!"
    }
}

let sample = Greeting.message(for: "SwiftLint")
let forced = sample as! NSString
print(sample)
print(forced)
