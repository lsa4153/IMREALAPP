import React from 'react';
import {View, Text, TouchableOpacity, StyleSheet} from 'react-native';
import {useNavigation, useRoute} from '@react-navigation/native';
import Icon from 'react-native-vector-icons/Feather';

export default function BottomNav() {
  const navigation = useNavigation<any>();
  const route = useRoute();

  const navItems = [
    {name: 'Home', icon: 'home', label: 'Home'},
    {name: 'Protect', icon: 'shield', label: '보호'},
    {name: 'History', icon: 'clock', label: '기록'},
    {name: 'News', icon: 'file-text', label: '뉴스'},
  ];

  return (
    <View style={styles.container}>
      {navItems.map(item => {
        const isActive = route.name === item.name;
        return (
          <TouchableOpacity
            key={item.name}
            style={styles.navItem}
            onPress={() => navigation.navigate(item.name)}
            activeOpacity={0.7}>
            <Icon
              name={item.icon}
              size={24}
              color={isActive ? '#7c3aed' : '#9ca3af'}
            />
            <Text
              style={[styles.navLabel, isActive && styles.navLabelActive]}>
              {item.label}
            </Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    paddingBottom: 8,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: -2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  navItem: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
  },
  navLabel: {
    fontSize: 11,
    marginTop: 4,
    color: '#9ca3af',
    fontWeight: '500',
  },
  navLabelActive: {
    color: '#7c3aed',
    fontWeight: '600',
  },
});