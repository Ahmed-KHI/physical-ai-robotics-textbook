import React from 'react';
import DocItemLayout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): React.JSX.Element {
  // Temporarily disabled personalization/translation buttons
  // Will add back after fixing content context access
  return <DocItemLayout {...props} />;
}
