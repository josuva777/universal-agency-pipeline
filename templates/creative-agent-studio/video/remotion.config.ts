import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setScale(2); // Native 2x render for pristine 4K quality
Config.setChromiumDisableWebSecurity(false);
Config.setOverwriteOutput(true);
