import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import { Send, Bot, User, Sparkles, AlertCircle } from 'lucide-react-native';
import * as Haptics from 'expo-haptics';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  isError?: boolean;
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'assistant',
      text: 'Hello! I am your mobile AI copilot. Send a message to query the backend or ask a workflow question.',
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const API_ENDPOINT = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:3000/api/chat';

  const handleSend = async () => {
    const trimmed = inputText.trim();
    if (!trimmed || isLoading) return;

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: trimmed,
    };

    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map((m) => ({
            role: m.sender,
            content: m.text,
          })),
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const responseText = await response.text();
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      const aiReply: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: responseText || 'Response received from AI endpoint.',
      };
      setMessages((prev) => [...prev, aiReply]);
    } catch (err: any) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      const errorReply: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: `Backend connection notice: Could not reach endpoint (${API_ENDPOINT}). Ensure your Next.js backend server is running ('npm run dev') or configure EXPO_PUBLIC_API_URL. (${err.message})`,
        isError: true,
      };
      setMessages((prev) => [...prev, errorReply]);
    } finally {
      setIsLoading(false);
    }
  };

  const renderItem = ({ item }: { item: Message }) => {
    const isAi = item.sender === 'assistant';
    return (
      <View style={[styles.messageRow, isAi ? styles.aiRow : styles.userRow]}>
        <View style={[styles.avatar, isAi ? styles.aiAvatar : styles.userAvatar]}>
          {isAi ? (
            item.isError ? (
              <AlertCircle size={16} color="#fb7185" />
            ) : (
              <Bot size={16} color="#06b6d4" />
            )
          ) : (
            <User size={16} color="#ffffff" />
          )}
        </View>
        <View
          style={[
            styles.bubble,
            isAi
              ? item.isError
                ? styles.errorBubble
                : styles.aiBubble
              : styles.userBubble,
          ]}
        >
          <Text
            style={[
              styles.messageText,
              isAi
                ? item.isError
                  ? styles.errorText
                  : styles.aiText
                : styles.userText,
            ]}
          >
            {item.text}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={80}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.statusDot} />
          <Text style={styles.headerTitle}>AI Mobile Assistant</Text>
        </View>
        <View style={styles.modelPill}>
          <Sparkles size={12} color="#06b6d4" />
          <Text style={styles.modelText}>Connected Backend</Text>
        </View>
      </View>

      {/* Message List */}
      <FlatList
        data={messages}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
      />

      {/* Input Bar */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Type an instruction or query..."
          placeholderTextColor="#475569"
          value={inputText}
          onChangeText={setInputText}
          editable={!isLoading}
          onSubmitEditing={handleSend}
          returnKeyType="send"
        />
        <TouchableOpacity
          style={[
            styles.sendButton,
            (!inputText.trim() || isLoading) && styles.sendButtonDisabled,
          ]}
          onPress={handleSend}
          disabled={!inputText.trim() || isLoading}
          activeOpacity={0.8}
        >
          {isLoading ? (
            <ActivityIndicator size="small" color="#000000" />
          ) : (
            <Send size={18} color="#000000" />
          )}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#090b10',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 54,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e2638',
    backgroundColor: '#0d111a',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#10b981',
  },
  headerTitle: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  modelPill: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(6, 182, 212, 0.1)',
    borderColor: 'rgba(6, 182, 212, 0.3)',
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    gap: 6,
  },
  modelText: {
    color: '#06b6d4',
    fontSize: 11,
    fontWeight: '600',
  },
  listContent: {
    padding: 20,
    gap: 16,
  },
  messageRow: {
    flexDirection: 'row',
    gap: 10,
    maxWidth: '85%',
  },
  aiRow: {
    alignSelf: 'flex-start',
  },
  userRow: {
    alignSelf: 'flex-end',
    flexDirection: 'row-reverse',
  },
  avatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 2,
  },
  aiAvatar: {
    backgroundColor: 'rgba(6, 182, 212, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(6, 182, 212, 0.3)',
  },
  userAvatar: {
    backgroundColor: '#6366f1',
  },
  bubble: {
    borderRadius: 18,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  aiBubble: {
    backgroundColor: '#111520',
    borderColor: '#1e2638',
    borderWidth: 1,
  },
  errorBubble: {
    backgroundColor: 'rgba(244, 63, 94, 0.1)',
    borderColor: 'rgba(244, 63, 94, 0.3)',
    borderWidth: 1,
  },
  userBubble: {
    backgroundColor: '#06b6d4',
  },
  messageText: {
    fontSize: 14,
    lineHeight: 20,
  },
  aiText: {
    color: '#e2e8f0',
  },
  errorText: {
    color: '#fda4af',
  },
  userText: {
    color: '#000000',
    fontWeight: '500',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    paddingBottom: Platform.OS === 'ios' ? 32 : 16,
    borderTopWidth: 1,
    borderTopColor: '#1e2638',
    backgroundColor: '#0d111a',
    gap: 12,
  },
  input: {
    flex: 1,
    backgroundColor: '#111520',
    borderColor: '#1e2638',
    borderWidth: 1,
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 12,
    color: '#ffffff',
    fontSize: 14,
  },
  sendButton: {
    backgroundColor: '#06b6d4',
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#1e2638',
    opacity: 0.5,
  },
});
