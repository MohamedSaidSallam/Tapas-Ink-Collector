# Tapas Ink Collector

[![GitHub Release][github_release_badge]][github_release_link]
[![License][license-image]][license-url]

A simple python script that uses adb to open tapas app, watch video ads and collect the ink reward for you. Then rinse and repeat.

> disclaimer: this is by no means an efficient or a good way for farming ink. Tapas pricing is reasonable that earning 10 ink per min (maybe even more than a min) is simply not worth it. I merely did this because I wanted to learn how to use ADB. The script is useful if you are short a hundred or so ink.

## Notes

* The values in the [config file][config-json] were tested on my [Samsung Galaxy J7 Pro](https://www.gsmarena.com/samsung_galaxy_j7_pro-8561.php) which has a 1920x1080 display
  * if your screen is different, The script might fail and in that case you need to change the config. Checkout the [Configuring](#configuring) section for more details.
* If you live in a region with little to no ads available on Tapas. I recommended using [cloudflare](https://1.1.1.1/). The Warp feature works as a VPN.

## Features

1. Automatically launches the app
1. Navigates to the free ink menu
1. Taps the watch video button
1. If there's no offers available it will wait for them to be available
1. Waits for a set amount then goes to the previous screen
1. Claims rewards
1. If an hour pasted since starting or the max amount of ads watched. It will restart the app
1. Repeats steps starting from step #3

## Prerequisites

You have to do the following before running the script:

* Connect your phone to your computer using USB.
* Enable USB debugging
* In the same settings menu, enable Stay Awake (or the screen will shut down while the script waits for the ads).
  * you can use [Screen Copy](https://github.com/Genymobile/scrcpy) to turn off your display

    ```sh
    scrcpy -S --max-fps 1
    ```

* Install python dependencies.

    ```sh
    py -m venv venv
    ./venv/Scripts/python -m pip install -r requirements.txt
    ```

## Running the script

```sh
./venv/Scripts/python -m tapas_ink_collector
```

## Configuring

A [Config.json][config-json] file is available at the root directory with the configuration to run the script. the following is the meaning of each field.

* `adb`: adb host & port. you probably don't need to change this.
* `appName`: tapas app name. used to launch the app.
  * you can get it through the following command

    ```sh
    adb shell pm list packages | grep tapas
    ```

* `colors`*: the rgb of certain parts of the UI the scripts checks for.
* `locations`*: the x & y of certain parts of the UI the script interacts with. You can get it either by
  * taking a screenshot of your phone and using paint (or any similar software) and reading the coordinates in the bottom left of paint.
  * or by enabling Pointer Location in Developer options in android
* `adSleepAmount`: time in seconds to wait for the ad to finish
* `maxTimes`: number of ads that can be watched per hour.

*: check out [ConfigMeaning.md](docs/ConfigMeaning.md) to find out what each value means.

## Authors

* **Mohamed Said Sallam** - Main Dev - [TheDigitalPhoenixX](https://github.com/TheDigitalPhoenixX)

See also the list of [contributors][github-contributors] who participated in this project and their work in [CONTRIBUTORS.md](CONTRIBUTORS.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [README.md Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

[license-image]: https://img.shields.io/badge/License-MIT-brightgreen.svg
[license-url]: https://opensource.org/licenses/MIT

[github_release_badge]: https://img.shields.io/github/v/release/TheDigitalPhoenixX/Tapas-Ink-Collector.svg?style=flat&include_prereleases
[github_release_link]: https://github.com/TheDigitalPhoenixX/Tapas-Ink-Collector/releases

[github-contributors]: https://github.com/TheDigitalPhoenixX/Tapas-Ink-Collector/contributors
[github-tags]: https://github.com/TheDigitalPhoenixX/Tapas-Ink-Collector/tags

[config-json]: config.json
