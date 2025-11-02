import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {StatusBar} from 'react-native';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import DetectScreen from './src/screens/DetectScreen';
import ProtectScreen from './src/screens/ProtectScreen';
import WatermarkScreen from './src/screens/WatermarkScreen';
import HistoryScreen from './src/screens/HistoryScreen';
import NewsScreen from './src/screens/NewsScreen';

const Stack = createNativeStackNavigator();

function App(): React.JSX.Element {
  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#7c3aed" />
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerShown: false,
        }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Detect" component={DetectScreen} />
        <Stack.Screen name="Protect" component={ProtectScreen} />
        <Stack.Screen name="Watermark" component={WatermarkScreen} />
        <Stack.Screen name="History" component={HistoryScreen} />
        <Stack.Screen name="News" component={NewsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;