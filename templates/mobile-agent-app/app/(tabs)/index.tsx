import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { Canvas, Circle, SweepGradient, vec } from '@shopify/react-native-skia';
import { ArrowRight, Zap, Shield, Sparkles } from 'lucide-react-native';
import * as Haptics from 'expo-haptics';

export default function HomeScreen() {
  const router = useRouter();

  const handleStartChat = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    router.push('/(tabs)/chat');
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* 3D Skia Glowing Orb Header */}
      <View style={styles.heroCanvasContainer}>
        <Canvas style={styles.canvas}>
          <Circle cx={120} cy={120} r={110}>
            <SweepGradient
              c={vec(120, 120)}
              colors={['#06b6d4', '#6366f1', '#d946ef', '#06b6d4']}
            />
          </Circle>
        </Canvas>
        <View style={styles.badge}>
          <Sparkles size={14} color="#06b6d4" />
          <Text style={styles.badgeText}>AUTONOMOUS AGENT ACTIVE</Text>
        </View>
      </View>

      {/* Hero Typography */}
      <View style={styles.textContainer}>
        <Text style={styles.headline}>INTELLIGENCE{'\n'}REDEFINED.</Text>
        <Text style={styles.subtext}>
          Powered by edge intelligence, hybrid RAG, and sub-50ms streaming responses.
        </Text>
      </View>

      {/* CTA Button */}
      <TouchableOpacity
        style={styles.ctaButton}
        onPress={handleStartChat}
        activeOpacity={0.85}
      >
        <Text style={styles.ctaText}>Launch AI Assistant</Text>
        <ArrowRight size={18} color="#000000" />
      </TouchableOpacity>

      {/* Metrics & Features Grid */}
      <View style={styles.grid}>
        <View style={styles.card}>
          <Zap size={20} color="#06b6d4" />
          <Text style={styles.cardValue}>&lt; 50ms</Text>
          <Text style={styles.cardLabel}>Latency</Text>
        </View>
        <View style={styles.card}>
          <Shield size={20} color="#6366f1" />
          <Text style={styles.cardValue}>100%</Text>
          <Text style={styles.cardLabel}>Zero-Leak Security</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#090b10',
  },
  content: {
    padding: 24,
    paddingTop: 60,
    alignItems: 'center',
  },
  heroCanvasContainer: {
    width: 240,
    height: 240,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
    position: 'relative',
  },
  canvas: {
    width: 240,
    height: 240,
  },
  badge: {
    position: 'absolute',
    bottom: -8,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(6, 182, 212, 0.15)',
    borderColor: 'rgba(6, 182, 212, 0.4)',
    borderWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    gap: 6,
  },
  badgeText: {
    color: '#06b6d4',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  },
  textContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  headline: {
    fontSize: 38,
    fontWeight: '900',
    color: '#ffffff',
    textAlign: 'center',
    letterSpacing: -1,
    lineHeight: 44,
  },
  subtext: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
    marginTop: 12,
    lineHeight: 20,
    maxWidth: 300,
  },
  ctaButton: {
    backgroundColor: '#ffffff',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 28,
    borderRadius: 14,
    width: '100%',
    gap: 10,
    marginBottom: 32,
    shadowColor: '#6366f1',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  ctaText: {
    color: '#000000',
    fontWeight: '800',
    fontSize: 15,
  },
  grid: {
    flexDirection: 'row',
    gap: 12,
    width: '100%',
  },
  card: {
    flex: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.04)',
    borderColor: 'rgba(255, 255, 255, 0.08)',
    borderWidth: 1,
    padding: 16,
    borderRadius: 14,
    alignItems: 'center',
    gap: 6,
  },
  cardValue: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: '800',
    marginTop: 4,
  },
  cardLabel: {
    color: '#64748b',
    fontSize: 11,
    fontWeight: '600',
  },
});

