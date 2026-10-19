# 📱 Turnkey Mobile Agent App

A high-performance mobile application template built with **Expo SDK 52**, **React Native Skia**, **Reanimated 3**, and streaming AI chat intelligence.

---

## ⚡ Quickstart

```bash
# 1. Install dependencies
npm install

# 2. Start Expo local development server
npm start

# 3. Run on device or simulator
npm run ios     # iOS Simulator
npm run android # Android Emulator
```

---

## 🧪 Automated Testing with Maestro

This template includes automated E2E test flows using **Maestro**:

```bash
# Run the automated chat flow test
maestro test .maestro/flows/chat.yaml
```

The test validates:
1. App launch and Skia canvas mount
2. Tab bar navigation to AI Chatbot
3. Keyboard input and streaming response rendering

---

## 📦 Tech Stack
- **Framework**: Expo SDK 52 (Expo Router v4)
- **Visuals**: `@shopify/react-native-skia` (60fps shaders & vector canvas)
- **Physics**: `react-native-reanimated` v3 (UI-thread animations)
- **Haptics**: `expo-haptics`
- **Testing**: Maestro E2E
