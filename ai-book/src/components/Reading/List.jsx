import React from 'react';
import clsx from 'clsx';
import styles from './List.module.css';

// Custom list component for consistent styling
const List = ({ children, ordered = false, className, ...props }) => {
  const ListTag = ordered ? 'ol' : 'ul';

  return (
    <ListTag
      className={clsx(
        styles.list,
        {[styles.ordered]: ordered},
        className
      )}
      {...props}
    >
      {children}
    </ListTag>
  );
};

// Individual list item component
const ListItem = ({ children, className, ...props }) => {
  return (
    <li
      className={clsx(
        styles.listItem,
        className
      )}
      {...props}
    >
      {children}
    </li>
  );
};

List.Item = ListItem;

export default List;